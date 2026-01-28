# GraphQL Best Practices

Comprehensive guidelines for building production-ready GraphQL APIs.

## Schema Design

### 1. Use Descriptive Names

**Good:**

```graphql
type User {
  id: ID!
  email: String!
  createdAt: DateTime!
}
```

**Bad:**

```graphql
type User {
  id: ID!
  e: String!
  ts: String!
}
```

### 2. Document Everything

```graphql
"""
Represents a user account in the system.
Users can create posts, comments, and like content.
"""
type User {
  """
  Unique identifier for the user.
  Format: UUID v4
  """
  id: ID!
  
  """
  User's email address. Must be unique.
  Validated according to RFC 5322
  """
  email: String!
  
  """
  Timestamp when the user account was created.
  Format: ISO 8601
  """
  createdAt: DateTime!
}
```

### 3. Use Appropriate Scalar Types

**Built-in Scalars:**

- `ID` - Unique identifiers (serialized as String)
- `String` - UTF-8 character sequences
- `Int` - Signed 32-bit integers
- `Float` - Signed double-precision floating-point values
- `Boolean` - true or false

**Custom Scalars:**

```graphql
scalar DateTime
scalar Email
scalar URL
scalar JSON
scalar Upload
```

### 4. Make Nullable vs Non-Null Explicit

**Rules:**

- Use `!` for guaranteed fields
- Omit `!` for optional fields
- Lists: `[Type!]!` usually most appropriate
  - Array is non-null
  - Items are non-null
  - Empty array is valid

### 5. Design for Evolution

```graphql
type User {
  id: ID!
  
  # Deprecated field
  name: String! @deprecated(reason: "Split into firstName and lastName")
  
  # New fields
  firstName: String!
  lastName: String!
}
```

## Query Design

### 1. Implement Pagination

**Always paginate lists:**

```graphql
type Query {
  # Good
  users(first: Int, after: String): UserConnection!
  
  # Bad
  allUsers: [User!]!
}
```

### 2. Provide Filtering

```graphql
input UserFilter {
  role: UserRole
  isActive: Boolean
  createdAfter: DateTime
  search: String
}

type Query {
  users(
    filter: UserFilter
    first: Int
    after: String
  ): UserConnection!
}
```

### 3. Enable Sorting

```graphql
enum UserSortField {
  CREATED_AT
  NAME
  EMAIL
}

enum SortOrder {
  ASC
  DESC
}

input UserSort {
  field: UserSortField!
  order: SortOrder!
}

type Query {
  users(
    sort: UserSort
    first: Int
    after: String
  ): UserConnection!
}
```

### 4. Use Fragments

```graphql
# Define reusable fragments
fragment UserBasics on User {
  id
  name
  email
}

fragment PostSummary on Post {
  id
  title
  createdAt
  author {
    ...UserBasics
  }
}

# Use in queries
query GetFeed {
  feed {
    ...PostSummary
    likeCount
  }
}
```

## Mutation Design

### 1. Use Input Types

```graphql
input CreatePostInput {
  title: String!
  content: String!
  tags: [String!]
}

type Mutation {
  createPost(input: CreatePostInput!): CreatePostPayload!
}
```

### 2. Return Payload Types

```graphql
type CreatePostPayload {
  post: Post
  errors: [Error!]
  clientMutationId: String
}

type Error {
  field: String
  message: String!
  code: String!
}

type Mutation {
  createPost(input: CreatePostInput!): CreatePostPayload!
}
```

**Benefits:**

- Can return related objects
- Provides error details
- Extensible (add new fields without breaking changes)

### 3. Name Mutations Clearly

```graphql
type Mutation {
  # Good: Action + object
  createPost(input: CreatePostInput!): CreatePostPayload!
  updatePost(id: ID!, input: UpdatePostInput!): UpdatePostPayload!
  deletePost(id: ID!): DeletePostPayload!
  publishPost(id: ID!): PublishPostPayload!
  
  # Bad: Vague names
  post(input: PostInput!): Post
  save(id: ID!): Boolean
}
```

### 4. Validate Inputs

```typescript
const resolvers = {
  Mutation: {
    createUser: async (parent, { input }, context) => {
      // Validate email
      if (!isValidEmail(input.email)) {
        return {
          errors: [{
            field: 'email',
            message: 'Invalid email format',
            code: 'INVALID_FORMAT'
          }]
        };
      }
      
      // Validate password strength
      if (input.password.length < 8) {
        return {
          errors: [{
            field: 'password',
            message: 'Password must be at least 8 characters',
            code: 'PASSWORD_TOO_SHORT'
          }]
        };
      }
      
      // Create user
      const user = await db.users.create({ data: input });
      
      return { user, errors: [] };
    }
  }
};
```

## Security Best Practices

### 1. Authentication

```typescript
const resolvers = {
  Query: {
    currentUser: (parent, args, context) => {
      // Check if user is authenticated
      if (!context.user) {
        throw new GraphQLError('Authentication required', {
          extensions: { code: 'UNAUTHENTICATED' }
        });
      }
      
      return context.user;
    }
  }
};
```

### 2. Authorization

```typescript
const resolvers = {
  Mutation: {
    deletePost: async (parent, { id }, context) => {
      const post = await db.posts.findUnique({ where: { id } });
      
      // Check ownership
      if (post.authorId !== context.user.id) {
        throw new GraphQLError('Not authorized to delete this post', {
          extensions: { code: 'FORBIDDEN' }
        });
      }
      
      await db.posts.delete({ where: { id } });
      return { success: true };
    }
  }
};
```

### 3. Rate Limiting

```typescript
import rateLimit from 'graphql-rate-limit';

const rateLimiter = rateLimit({
  identifyContext: (ctx) => ctx.user?.id || ctx.ip
});

const resolvers = {
  Query: {
    search: rateLimiter({
      max: 10,
      window: '1m'
    }, async (parent, args) => {
      return performSearch(args.query);
    })
  }
};
```

### 4. Query Depth Limiting

```typescript
import depthLimit from 'graphql-depth-limit';

const server = new ApolloServer({
  typeDefs,
  resolvers,
  validationRules: [depthLimit(7)]
});
```

### 5. Query Complexity Analysis

```typescript
import { createComplexityLimitRule } from 'graphql-validation-complexity';

const server = new ApolloServer({
  typeDefs,
  resolvers,
  validationRules: [
    createComplexityLimitRule(1000)
  ]
});
```

### 6. Sanitize Errors

```typescript
import { ApolloServer } from '@apollo/server';

const server = new ApolloServer({
  typeDefs,
  resolvers,
  formatError: (formattedError, error) => {
    // Don't expose internal errors to clients
    if (error.extensions?.code === 'INTERNAL_SERVER_ERROR') {
      console.error('Internal error:', error);
      return new GraphQLError('An error occurred', {
        extensions: { code: 'INTERNAL_SERVER_ERROR' }
      });
    }
    
    return formattedError;
  }
});
```

### 7. Input Validation

```typescript
import { z } from 'zod';

const createUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(2).max(100),
  password: z.string().min(8)
});

const resolvers = {
  Mutation: {
    createUser: async (parent, { input }) => {
      // Validate with Zod
      const result = createUserSchema.safeParse(input);
      
      if (!result.success) {
        return {
          errors: result.error.issues.map(issue => ({
            field: issue.path.join('.'),
            message: issue.message,
            code: 'VALIDATION_ERROR'
          }))
        };
      }
      
      // Proceed with creation
      const user = await db.users.create({ data: result.data });
      return { user, errors: [] };
    }
  }
};
```

## Performance Best Practices

### 1. Use DataLoader

```typescript
import DataLoader from 'dataloader';

const createLoaders = () => ({
  user: new DataLoader(async (ids) => {
    const users = await db.users.findMany({
      where: { id: { in: ids } }
    });
    const userMap = new Map(users.map(u => [u.id, u]));
    return ids.map(id => userMap.get(id));
  }),
  
  post: new DataLoader(async (ids) => {
    const posts = await db.posts.findMany({
      where: { id: { in: ids } }
    });
    const postMap = new Map(posts.map(p => [p.id, p]));
    return ids.map(id => postMap.get(id));
  })
});

// In context
const context = {
  loaders: createLoaders()
};
```

### 2. Implement Caching

```typescript
import { ApolloServer } from '@apollo/server';
import responseCachePlugin from '@apollo/server-plugin-response-cache';

const server = new ApolloServer({
  typeDefs,
  resolvers,
  plugins: [responseCachePlugin()]
});

// In schema
const typeDefs = `
  type Query {
    # Cache for 1 hour
    publicStats: Stats @cacheControl(maxAge: 3600)
    
    # Don't cache
    currentUser: User @cacheControl(maxAge: 0, scope: PRIVATE)
  }
`;
```

### 3. Optimize Database Queries

```typescript
// Bad: Multiple queries
const posts = await db.posts.findMany();
for (const post of posts) {
  post.author = await db.users.findUnique({ 
    where: { id: post.authorId } 
  });
}

// Good: Single query with join
const posts = await db.posts.findMany({
  include: { author: true }
});
```

### 4. Batch Database Operations

```typescript
// Bad: Multiple insert operations
for (const post of posts) {
  await db.posts.create({ data: post });
}

// Good: Batch insert
await db.posts.createMany({
  data: posts
});
```

## Error Handling

### 1. Use Standard Error Codes

```typescript
enum ErrorCode {
  UNAUTHENTICATED = 'UNAUTHENTICATED',
  FORBIDDEN = 'FORBIDDEN',
  NOT_FOUND = 'NOT_FOUND',
  VALIDATION_ERROR = 'VALIDATION_ERROR',
  INTERNAL_SERVER_ERROR = 'INTERNAL_SERVER_ERROR'
}

throw new GraphQLError('Resource not found', {
  extensions: {
    code: ErrorCode.NOT_FOUND,
    resourceType: 'Post',
    resourceId: id
  }
});
```

### 2. Provide Helpful Error Messages

```typescript
// Bad
throw new Error('Error');

// Good
throw new GraphQLError('Post with id "123" not found', {
  extensions: {
    code: 'NOT_FOUND',
    resource: 'Post',
    id: '123'
  }
});
```

### 3. Use Error Extensions

```typescript
throw new GraphQLError('Validation failed', {
  extensions: {
    code: 'VALIDATION_ERROR',
    validationErrors: [
      { field: 'email', message: 'Invalid email format' },
      { field: 'password', message: 'Password too short' }
    ]
  }
});
```

## Testing

### 1. Test Resolvers

```typescript
import { describe, it, expect } from 'vitest';

describe('User resolvers', () => {
  it('creates a user', async () => {
    const result = await resolvers.Mutation.createUser(
      null,
      {
        input: {
          email: 'test@example.com',
          name: 'Test User',
          password: 'password123'
        }
      },
      { db: mockDb }
    );
    
    expect(result.user).toBeDefined();
    expect(result.user.email).toBe('test@example.com');
    expect(result.errors).toHaveLength(0);
  });
});
```

### 2. Test Queries End-to-End

```typescript
import { ApolloServer } from '@apollo/server';

describe('GraphQL API', () => {
  const server = new ApolloServer({ typeDefs, resolvers });
  
  it('fetches user by id', async () => {
    const result = await server.executeOperation({
      query: `
        query GetUser($id: ID!) {
          user(id: $id) {
            id
            email
            name
          }
        }
      `,
      variables: { id: '1' }
    });
    
    expect(result.body.kind).toBe('single');
    expect(result.body.singleResult.data.user).toBeDefined();
  });
});
```

### 3. Test Authorization

```typescript
it('prevents unauthorized access', async () => {
  const result = await server.executeOperation(
    {
      query: `
        mutation DeletePost($id: ID!) {
          deletePost(id: $id) {
            success
          }
        }
      `,
      variables: { id: '1' }
    },
    {
      contextValue: { user: null } // No authenticated user
    }
  );
  
  expect(result.body.kind).toBe('single');
  expect(result.body.singleResult.errors).toBeDefined();
  expect(result.body.singleResult.errors[0].extensions.code)
    .toBe('UNAUTHENTICATED');
});
```

## Documentation

### 1. Use Schema Descriptions

```graphql
"""
Main query entry point for the API.
"""
type Query {
  """
  Fetch a user by their unique identifier.
  
  Returns null if the user doesn't exist or the current user
  doesn't have permission to view them.
  """
  user(
    """User's unique ID"""
    id: ID!
  ): User
}
```

### 2. Provide Examples

```graphql
"""
Create a new blog post.

Example:
```

mutation {
  createPost(input: {
    title: "My First Post"
    content: "Hello, world!"
    tags: ["introduction", "blog"]
  }) {
    post {
      id
      title
    }
  }
}

```
"""
createPost(input: CreatePostInput!): CreatePostPayload!
```

### 3. Document Error Scenarios

```graphql
"""
Delete a post by ID.

Errors:
- NOT_FOUND: Post doesn't exist
- FORBIDDEN: User doesn't own the post
- UNAUTHENTICATED: User is not logged in

Returns:
- success: true if deleted successfully
- errors: Array of error details if failed
"""
deletePost(id: ID!): DeletePostPayload!
```

## Monitoring

### 1. Log Slow Queries

```typescript
const performancePlugin = {
  async requestDidStart() {
    const start = Date.now();
    
    return {
      async willSendResponse({ request, response }) {
        const duration = Date.now() - start;
        
        if (duration > 1000) {
          console.warn('Slow query:', {
            duration,
            query: request.query,
            variables: request.variables
          });
        }
      }
    };
  }
};
```

### 2. Track Error Rates

```typescript
let errorCount = 0;

const errorTrackingPlugin = {
  async requestDidStart() {
    return {
      async didEncounterErrors({ errors }) {
        errorCount += errors.length;
        
        errors.forEach(error => {
          console.error('GraphQL error:', {
            message: error.message,
            code: error.extensions?.code,
            path: error.path
          });
        });
      }
    };
  }
};
```

### 3. Monitor Query Complexity

```typescript
const complexityPlugin = {
  async requestDidStart({ request }) {
    const complexity = calculateComplexity(request.query);
    
    console.log('Query complexity:', complexity);
    
    if (complexity > 500) {
      console.warn('High complexity query detected');
    }
  }
};
```

## Checklist

- [ ] All types and fields documented
- [ ] Pagination implemented for lists
- [ ] DataLoader used for relationships
- [ ] Authentication implemented
- [ ] Authorization enforced
- [ ] Rate limiting configured
- [ ] Query depth limiting enabled
- [ ] Errors sanitized for production
- [ ] Input validation implemented
- [ ] Tests written for critical paths
- [ ] Monitoring and logging configured
- [ ] Performance optimized
- [ ] Documentation complete
- [ ] API versioning strategy defined
