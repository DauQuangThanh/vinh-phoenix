# GraphQL Query Optimization Guide

This guide covers strategies for optimizing GraphQL query performance and preventing common performance issues.

## Common Performance Problems

### 1. N+1 Query Problem

**Problem:** Fetching a list of items and then making separate queries for each item's related data.

**Example:**

```graphql
query GetPosts {
  posts {
    id
    title
    author {  # Separate query for EACH post!
      name
    }
  }
}
```

**Without optimization:**

```
1 query: SELECT * FROM posts;
N queries: SELECT * FROM users WHERE id = ?; (for each post)
Total: 1 + N queries
```

**Solution: DataLoader**

```typescript
import DataLoader from 'dataloader';

// Create DataLoader
const userLoader = new DataLoader(async (userIds: readonly string[]) => {
  // Single batched query
  const users = await db.users.findMany({
    where: { id: { in: [...userIds] } }
  });
  
  // Return in same order as requested
  const userMap = new Map(users.map(u => [u.id, u]));
  return userIds.map(id => userMap.get(id) || null);
});

// Use in context
const context = {
  loaders: {
    user: userLoader
  }
};

// Use in resolver
const resolvers = {
  Post: {
    author: (post, args, { loaders }) => {
      return loaders.user.load(post.authorId);
    }
  }
};
```

**Result:**

```
1 query: SELECT * FROM posts;
1 query: SELECT * FROM users WHERE id IN (1, 2, 3, ...);
Total: 2 queries
```

### 2. Over-Fetching Data

**Problem:** Selecting all columns when only some are needed.

**Bad:**

```typescript
// Resolver fetches all user data
const resolvers = {
  Query: {
    users: () => {
      return db.users.findMany(); // SELECT *
    }
  }
};
```

**Good: Use Field Selection**

```typescript
import { GraphQLResolveInfo } from 'graphql';
import { parseResolveInfo } from 'graphql-parse-resolve-info';

const resolvers = {
  Query: {
    users: (parent, args, context, info: GraphQLResolveInfo) => {
      const fields = getFieldNames(info);
      
      return db.users.findMany({
        select: {
          id: fields.includes('id'),
          name: fields.includes('name'),
          email: fields.includes('email'),
          // Only select requested fields
        }
      });
    }
  }
};

function getFieldNames(info: GraphQLResolveInfo): string[] {
  const parsed = parseResolveInfo(info);
  return Object.keys(parsed?.fieldsByTypeName?.User || {});
}
```

### 3. Deeply Nested Queries

**Problem:** Queries can nest infinitely, causing exponential resource usage.

**Dangerous Query:**

```graphql
query DeepQuery {
  user(id: "1") {
    friends {
      friends {
        friends {
          friends {
            friends {
              # Can go on forever!
            }
          }
        }
      }
    }
  }
}
```

**Solution 1: Query Depth Limiting**

```typescript
import { createComplexityLimitRule } from 'graphql-validation-complexity';

const server = new ApolloServer({
  typeDefs,
  resolvers,
  validationRules: [
    createComplexityLimitRule(1000, {
      onCost: (cost) => {
        console.log('Query cost:', cost);
      }
    })
  ]
});
```

**Solution 2: Maximum Depth Plugin**

```typescript
import depthLimit from 'graphql-depth-limit';

const server = new ApolloServer({
  typeDefs,
  resolvers,
  validationRules: [depthLimit(5)] // Max 5 levels deep
});
```

### 4. Large Result Sets

**Problem:** Returning thousands of items without pagination.

**Bad:**

```graphql
type Query {
  allPosts: [Post!]!  # Could return 100,000 posts!
}
```

**Good: Implement Pagination**

```graphql
type Query {
  posts(
    first: Int = 10
    after: String
  ): PostConnection!
}

type PostConnection {
  edges: [PostEdge!]!
  pageInfo: PageInfo!
}
```

**Resolver with efficient pagination:**

```typescript
const resolvers = {
  Query: {
    posts: async (parent, { first = 10, after }) => {
      // Decode cursor
      const offset = after ? parseInt(decodeCursor(after)) : 0;
      
      // Fetch one extra to check if there's more
      const posts = await db.posts.findMany({
        skip: offset,
        take: first + 1,
        orderBy: { createdAt: 'desc' }
      });
      
      const hasNextPage = posts.length > first;
      const edges = posts.slice(0, first).map((post, index) => ({
        node: post,
        cursor: encodeCursor(offset + index)
      }));
      
      return {
        edges,
        pageInfo: {
          hasNextPage,
          endCursor: edges[edges.length - 1]?.cursor || null
        }
      };
    }
  }
};
```

## Optimization Strategies

### Strategy 1: Query Complexity Analysis

Assign costs to fields and reject expensive queries.

```typescript
import { createComplexityLimitRule } from 'graphql-validation-complexity';

const complexityRule = createComplexityLimitRule(1000, {
  scalarCost: 1,
  objectCost: 2,
  listFactor: 10,
  introspectionListFactor: 2,
  
  // Custom costs for specific fields
  fieldCost: (args, childCost, ctx) => {
    const { field } = ctx;
    
    // Expensive operations
    if (field.name === 'search') {
      return 50 + childCost;
    }
    
    // Lists multiply child cost by requested items
    if (field.name === 'posts' && args.first) {
      return args.first * childCost;
    }
    
    return childCost;
  }
});
```

### Strategy 2: Field-Level Caching

Cache expensive computations.

**Using Apollo Server:**

```typescript
import { ApolloServer } from '@apollo/server';
import responseCachePlugin from '@apollo/server-plugin-response-cache';

const server = new ApolloServer({
  typeDefs,
  resolvers,
  plugins: [
    responseCachePlugin({
      sessionId: (requestContext) => {
        return requestContext.request.http?.headers.get('session-id') || null;
      }
    })
  ]
});

// In schema
const typeDefs = `
  type Query {
    expensiveCalculation: Float! @cacheControl(maxAge: 3600)
    currentUser: User @cacheControl(scope: PRIVATE, maxAge: 60)
  }
`;
```

**Custom caching in resolvers:**

```typescript
import Redis from 'ioredis';

const redis = new Redis();

const resolvers = {
  Query: {
    stats: async () => {
      const cacheKey = 'stats:global';
      
      // Check cache
      const cached = await redis.get(cacheKey);
      if (cached) {
        return JSON.parse(cached);
      }
      
      // Calculate
      const stats = await calculateExpensiveStats();
      
      // Cache for 5 minutes
      await redis.setex(cacheKey, 300, JSON.stringify(stats));
      
      return stats;
    }
  }
};
```

### Strategy 3: Persisted Queries

Reduce payload size and improve performance.

**Client:**

```typescript
import { createPersistedQueryLink } from '@apollo/client/link/persisted-queries';
import { sha256 } from 'crypto-hash';

const link = createPersistedQueryLink({ sha256 });
```

**Server:**

```typescript
import { ApolloServer } from '@apollo/server';

const server = new ApolloServer({
  typeDefs,
  resolvers,
  persistedQueries: {
    cache: redis, // Use Redis for query storage
  }
});
```

**Benefits:**

- Smaller network payload (just send hash)
- Automatic query whitelisting
- Better CDN caching

### Strategy 4: Query Batching

Combine multiple queries into one request.

**Client:**

```typescript
import { ApolloClient, HttpLink } from '@apollo/client';
import { BatchHttpLink } from '@apollo/client/link/batch-http';

const link = new BatchHttpLink({
  uri: 'http://localhost:4000/graphql',
  batchMax: 10, // Max 10 queries per batch
  batchInterval: 20 // Wait 20ms before sending
});

const client = new ApolloClient({
  link,
  cache: new InMemoryCache()
});
```

### Strategy 5: Automatic Persisted Queries (APQ)

**Enable on server:**

```typescript
import { ApolloServer } from '@apollo/server';

const server = new ApolloServer({
  typeDefs,
  resolvers,
  persistedQueries: {
    ttl: 900 // Cache for 15 minutes
  }
});
```

**Client automatically uses APQ:**

```typescript
import { createPersistedQueryLink } from '@apollo/client/link/persisted-queries';
import { sha256 } from 'crypto-hash';

const link = createPersistedQueryLink({ sha256 });
```

## Monitoring and Profiling

### Track Resolver Performance

```typescript
import { GraphQLResolveInfo } from 'graphql';

const resolvers = {
  Query: {
    posts: async (parent, args, context, info: GraphQLResolveInfo) => {
      const start = Date.now();
      
      try {
        const result = await db.posts.findMany();
        return result;
      } finally {
        const duration = Date.now() - start;
        console.log(`posts resolver took ${duration}ms`);
        
        // Send to monitoring
        metrics.recordResolverTime('Query.posts', duration);
      }
    }
  }
};
```

### Apollo Studio Integration

```typescript
import { ApolloServer } from '@apollo/server';
import { ApolloServerPluginUsageReporting } from '@apollo/server/plugin/usageReporting';

const server = new ApolloServer({
  typeDefs,
  resolvers,
  plugins: [
    ApolloServerPluginUsageReporting({
      sendVariableValues: { all: true },
      sendHeaders: { all: true }
    })
  ]
});
```

### Custom Performance Monitoring

```typescript
const performancePlugin = {
  async requestDidStart() {
    const start = Date.now();
    
    return {
      async willSendResponse({ response }) {
        const duration = Date.now() - start;
        
        // Log slow queries
        if (duration > 1000) {
          console.warn('Slow query detected:', {
            duration,
            query: request.query,
            variables: request.variables
          });
        }
        
        // Track metrics
        metrics.recordQueryDuration(duration);
      }
    };
  }
};
```

## Query Optimization Checklist

- [ ] DataLoader implemented for all relationships
- [ ] Query depth limiting enabled (max 5-7 levels)
- [ ] Query complexity analysis configured
- [ ] Pagination implemented for all lists
- [ ] Field-level caching for expensive operations
- [ ] Database queries optimized (proper indexes)
- [ ] N+1 queries eliminated
- [ ] Over-fetching minimized
- [ ] Response size monitoring enabled
- [ ] Slow query logging configured
- [ ] Rate limiting implemented
- [ ] Connection pooling configured
- [ ] CDN caching for public queries

## Database Optimization Tips

### Use Proper Indexes

```sql
-- Index for filtering
CREATE INDEX idx_posts_published ON posts(published);

-- Composite index for common queries
CREATE INDEX idx_posts_author_created ON posts(author_id, created_at DESC);

-- Index for sorting
CREATE INDEX idx_posts_created ON posts(created_at DESC);
```

### Optimize Join Queries

```typescript
// Instead of N+1 queries
const posts = await db.posts.findMany();
for (const post of posts) {
  post.author = await db.users.findUnique({ where: { id: post.authorId } });
}

// Use a single join
const posts = await db.posts.findMany({
  include: {
    author: true
  }
});
```

### Use Query Explain Plans

```typescript
// Log query plans in development
if (process.env.NODE_ENV === 'development') {
  await db.$on('query', (e) => {
    console.log('Query:', e.query);
    console.log('Duration:', e.duration);
  });
}
```

## Performance Benchmarks

Target response times:

- Simple queries: < 100ms
- Complex queries: < 500ms
- Paginated lists: < 200ms
- Mutations: < 300ms

Monitor and alert on queries exceeding these thresholds.
