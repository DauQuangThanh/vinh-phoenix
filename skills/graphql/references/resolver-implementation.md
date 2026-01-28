# GraphQL Resolver Implementation Guide

This guide provides detailed patterns for implementing GraphQL resolvers with proper data loading, error handling, and optimization.

## Basic Resolver Structure

### Query Resolvers

```typescript
const resolvers = {
  Query: {
    // Simple field resolver
    user: async (parent, { id }, context) => {
      return context.dataSources.users.findById(id);
    },
    
    // Resolver with pagination
    posts: async (parent, { first = 10, after }, context) => {
      const offset = after ? parseInt(decodeCursor(after)) : 0;
      const posts = await context.db.posts.findMany({
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

### Mutation Resolvers

```typescript
const resolvers = {
  Mutation: {
    createPost: async (parent, { input }, context) => {
      // 1. Authentication check
      if (!context.user) {
        throw new GraphQLError('Authentication required', {
          extensions: { code: 'UNAUTHENTICATED' }
        });
      }
      
      // 2. Input validation
      if (!input.title || input.title.length === 0) {
        throw new GraphQLError('Title is required', {
          extensions: {
            code: 'VALIDATION_ERROR',
            field: 'title'
          }
        });
      }
      
      // 3. Authorization check
      if (!context.user.canCreatePost) {
        throw new GraphQLError('Insufficient permissions', {
          extensions: { code: 'FORBIDDEN' }
        });
      }
      
      // 4. Business logic
      const post = await context.db.posts.create({
        data: {
          ...input,
          authorId: context.user.id
        }
      });
      
      return post;
    },
    
    updatePost: async (parent, { id, input }, context) => {
      if (!context.user) {
        throw new GraphQLError('Authentication required', {
          extensions: { code: 'UNAUTHENTICATED' }
        });
      }
      
      const post = await context.db.posts.findUnique({ where: { id } });
      
      if (!post) {
        throw new GraphQLError(`Post with id ${id} not found`, {
          extensions: { code: 'NOT_FOUND', resource: 'Post', id }
        });
      }
      
      if (post.authorId !== context.user.id) {
        throw new GraphQLError('Not authorized to update this post', {
          extensions: { code: 'FORBIDDEN' }
        });
      }
      
      return context.db.posts.update({
        where: { id },
        data: input
      });
    }
  }
};
```

### Type Resolvers

```typescript
const resolvers = {
  User: {
    // Resolve posts for a user using DataLoader
    posts: async (user, { first = 10, after }, context) => {
      const offset = after ? parseInt(decodeCursor(after)) : 0;
      
      const posts = await context.db.posts.findMany({
        where: { authorId: user.id },
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
        pageInfo: { hasNextPage, endCursor: edges[edges.length - 1]?.cursor }
      };
    },
    
    // Computed field
    fullName: (user) => {
      return `${user.firstName} ${user.lastName}`;
    },
    
    // Field with expensive calculation (cached)
    stats: async (user, args, context) => {
      const cacheKey = `user:${user.id}:stats`;
      const cached = await context.redis.get(cacheKey);
      
      if (cached) {
        return JSON.parse(cached);
      }
      
      const stats = await calculateUserStats(user.id, context.db);
      await context.redis.setex(cacheKey, 300, JSON.stringify(stats));
      
      return stats;
    }
  },
  
  Post: {
    // Resolve author using DataLoader (prevents N+1)
    author: (post, args, context) => {
      return context.loaders.user.load(post.authorId);
    },
    
    // Resolve likes count
    likesCount: async (post, args, context) => {
      return context.db.likes.count({
        where: { postId: post.id }
      });
    },
    
    // Computed field based on context
    isLikedByMe: async (post, args, context) => {
      if (!context.user) return false;
      
      const like = await context.db.likes.findUnique({
        where: {
          userId_postId: {
            userId: context.user.id,
            postId: post.id
          }
        }
      });
      
      return !!like;
    }
  }
};
```

## DataLoader Implementation

### Creating DataLoaders

```typescript
import DataLoader from 'dataloader';

// User loader
const createUserLoader = (db) => {
  return new DataLoader(async (userIds: readonly string[]) => {
    const users = await db.users.findMany({
      where: { id: { in: [...userIds] } }
    });
    
    // Return in same order as requested
    const userMap = new Map(users.map(u => [u.id, u]));
    return userIds.map(id => userMap.get(id) || null);
  });
};

// Post loader
const createPostLoader = (db) => {
  return new DataLoader(async (postIds: readonly string[]) => {
    const posts = await db.posts.findMany({
      where: { id: { in: [...postIds] } }
    });
    
    const postMap = new Map(posts.map(p => [p.id, p]));
    return postIds.map(id => postMap.get(id) || null);
  });
};

// Posts by user loader (one-to-many)
const createPostsByUserLoader = (db) => {
  return new DataLoader(async (userIds: readonly string[]) => {
    const posts = await db.posts.findMany({
      where: { authorId: { in: [...userIds] } }
    });
    
    // Group by user
    const postsByUser = new Map<string, Post[]>();
    for (const post of posts) {
      const userPosts = postsByUser.get(post.authorId) || [];
      userPosts.push(post);
      postsByUser.set(post.authorId, userPosts);
    }
    
    return userIds.map(id => postsByUser.get(id) || []);
  });
};

// Create loaders for context
export const createLoaders = (db) => ({
  user: createUserLoader(db),
  post: createPostLoader(db),
  postsByUser: createPostsByUserLoader(db)
});
```

### Using DataLoaders in Context

```typescript
import { ApolloServer } from '@apollo/server';
import { createLoaders } from './loaders';

const server = new ApolloServer({
  typeDefs,
  resolvers,
  context: async ({ req }) => {
    const token = req.headers.authorization?.replace('Bearer ', '');
    const user = await validateToken(token);
    
    return {
      user,
      db,
      loaders: createLoaders(db), // Fresh loaders per request
      redis
    };
  }
});
```

### Using DataLoaders in Resolvers

```typescript
const resolvers = {
  Post: {
    author: (post, args, { loaders }) => {
      return loaders.user.load(post.authorId);
    }
  },
  
  User: {
    posts: (user, args, { loaders }) => {
      return loaders.postsByUser.load(user.id);
    }
  }
};
```

## Authentication & Authorization Patterns

### Context-Based Authentication

```typescript
// Context creation
context: async ({ req }) => {
  const token = req.headers.authorization?.replace('Bearer ', '');
  
  if (!token) {
    return { user: null, db, loaders: createLoaders(db) };
  }
  
  try {
    const payload = jwt.verify(token, JWT_SECRET);
    const user = await db.users.findUnique({ where: { id: payload.userId } });
    
    return { user, db, loaders: createLoaders(db) };
  } catch (error) {
    return { user: null, db, loaders: createLoaders(db) };
  }
}
```

### Resolver-Level Authorization

```typescript
const resolvers = {
  Query: {
    adminPanel: (parent, args, { user }) => {
      if (!user) {
        throw new GraphQLError('Authentication required', {
          extensions: { code: 'UNAUTHENTICATED' }
        });
      }
      
      if (!user.roles.includes('admin')) {
        throw new GraphQLError('Insufficient permissions', {
          extensions: { code: 'FORBIDDEN', requiredRole: 'admin' }
        });
      }
      
      return getAdminData();
    }
  },
  
  Mutation: {
    deleteUser: async (parent, { id }, { user, db }) => {
      if (!user) {
        throw new GraphQLError('Authentication required', {
          extensions: { code: 'UNAUTHENTICATED' }
        });
      }
      
      // Check if deleting self or has admin permission
      if (id !== user.id && !user.roles.includes('admin')) {
        throw new GraphQLError('Can only delete your own account', {
          extensions: { code: 'FORBIDDEN' }
        });
      }
      
      await db.users.delete({ where: { id } });
      return true;
    }
  }
};
```

### Directive-Based Authorization

```typescript
import { mapSchema, getDirective, MapperKind } from '@graphql-tools/utils';

function authDirective(directiveName: string) {
  return {
    authDirectiveTypeDefs: `directive @${directiveName}(requires: Role) on FIELD_DEFINITION`,
    
    authDirectiveTransformer: (schema) =>
      mapSchema(schema, {
        [MapperKind.OBJECT_FIELD]: (fieldConfig) => {
          const directive = getDirective(schema, fieldConfig, directiveName)?.[0];
          
          if (directive) {
            const { requires } = directive;
            const { resolve = defaultFieldResolver } = fieldConfig;
            
            fieldConfig.resolve = async (source, args, context, info) => {
              if (!context.user) {
                throw new GraphQLError('Authentication required', {
                  extensions: { code: 'UNAUTHENTICATED' }
                });
              }
              
              if (!context.user.roles.includes(requires)) {
                throw new GraphQLError(`Requires ${requires} role`, {
                  extensions: { code: 'FORBIDDEN', requiredRole: requires }
                });
              }
              
              return resolve(source, args, context, info);
            };
          }
          
          return fieldConfig;
        }
      })
  };
}

// Usage in schema
const typeDefs = `
  enum Role {
    USER
    ADMIN
    MODERATOR
  }
  
  type Query {
    users: [User!]! @auth(requires: ADMIN)
    me: User
  }
`;
```

## Error Handling Patterns

### Standard Error Codes

```typescript
enum ErrorCode {
  UNAUTHENTICATED = 'UNAUTHENTICATED',
  FORBIDDEN = 'FORBIDDEN',
  NOT_FOUND = 'NOT_FOUND',
  VALIDATION_ERROR = 'VALIDATION_ERROR',
  CONFLICT = 'CONFLICT',
  INTERNAL_SERVER_ERROR = 'INTERNAL_SERVER_ERROR'
}

// Helper function
function throwGraphQLError(message: string, code: ErrorCode, extensions = {}) {
  throw new GraphQLError(message, {
    extensions: { code, ...extensions }
  });
}
```

### Validation Error Handling

```typescript
import { z } from 'zod';

const createPostSchema = z.object({
  title: z.string().min(1).max(200),
  content: z.string().min(1),
  tags: z.array(z.string()).max(10)
});

const resolvers = {
  Mutation: {
    createPost: async (parent, { input }, context) => {
      // Validate with Zod
      const result = createPostSchema.safeParse(input);
      
      if (!result.success) {
        const errors = result.error.issues.map(issue => ({
          field: issue.path.join('.'),
          message: issue.message
        }));
        
        throw new GraphQLError('Validation failed', {
          extensions: {
            code: 'VALIDATION_ERROR',
            validationErrors: errors
          }
        });
      }
      
      // Proceed with creation
      return context.db.posts.create({ data: result.data });
    }
  }
};
```

### Try-Catch Error Handling

```typescript
const resolvers = {
  Query: {
    user: async (parent, { id }, context) => {
      try {
        const user = await context.db.users.findUnique({ where: { id } });
        
        if (!user) {
          throw new GraphQLError(`User with id ${id} not found`, {
            extensions: { code: 'NOT_FOUND', resource: 'User', id }
          });
        }
        
        return user;
      } catch (error) {
        if (error instanceof GraphQLError) {
          throw error;
        }
        
        // Log internal errors
        console.error('Database error:', error);
        
        // Return sanitized error
        throw new GraphQLError('Failed to fetch user', {
          extensions: { code: 'INTERNAL_SERVER_ERROR' }
        });
      }
    }
  }
};
```

## Helper Functions

### Cursor Encoding/Decoding

```typescript
export function encodeCursor(offset: number): string {
  return Buffer.from(offset.toString()).toString('base64');
}

export function decodeCursor(cursor: string): string {
  return Buffer.from(cursor, 'base64').toString('utf-8');
}
```

### Pagination Helper

```typescript
interface PaginationArgs {
  first?: number;
  after?: string;
  last?: number;
  before?: string;
}

interface PaginationResult<T> {
  edges: Array<{ node: T; cursor: string }>;
  pageInfo: {
    hasNextPage: boolean;
    hasPreviousPage: boolean;
    startCursor: string | null;
    endCursor: string | null;
  };
}

export async function paginate<T>(
  query: any,
  args: PaginationArgs,
  defaultLimit = 10
): Promise<PaginationResult<T>> {
  const { first = defaultLimit, after } = args;
  const offset = after ? parseInt(decodeCursor(after)) : 0;
  
  const items = await query.skip(offset).take(first + 1);
  
  const hasNextPage = items.length > first;
  const edges = items.slice(0, first).map((item, index) => ({
    node: item,
    cursor: encodeCursor(offset + index)
  }));
  
  return {
    edges,
    pageInfo: {
      hasNextPage,
      hasPreviousPage: offset > 0,
      startCursor: edges[0]?.cursor || null,
      endCursor: edges[edges.length - 1]?.cursor || null
    }
  };
}
```

## Testing Resolvers

### Unit Testing

```typescript
import { describe, it, expect, vi } from 'vitest';

describe('User resolvers', () => {
  it('fetches user by id', async () => {
    const mockDb = {
      users: {
        findUnique: vi.fn().mockResolvedValue({
          id: '1',
          email: 'test@example.com'
        })
      }
    };
    
    const result = await resolvers.Query.user(
      null,
      { id: '1' },
      { db: mockDb, user: null, loaders: {} }
    );
    
    expect(result.id).toBe('1');
    expect(mockDb.users.findUnique).toHaveBeenCalledWith({ where: { id: '1' } });
  });
  
  it('throws error when user not found', async () => {
    const mockDb = {
      users: {
        findUnique: vi.fn().mockResolvedValue(null)
      }
    };
    
    await expect(
      resolvers.Query.user(null, { id: '999' }, { db: mockDb })
    ).rejects.toThrow('User with id 999 not found');
  });
});
```

### Integration Testing

```typescript
import { ApolloServer } from '@apollo/server';

describe('GraphQL API', () => {
  let server: ApolloServer;
  
  beforeAll(async () => {
    server = new ApolloServer({ typeDefs, resolvers });
  });
  
  it('creates a post', async () => {
    const result = await server.executeOperation({
      query: `
        mutation CreatePost($input: CreatePostInput!) {
          createPost(input: $input) {
            id
            title
            content
          }
        }
      `,
      variables: {
        input: {
          title: 'Test Post',
          content: 'Test content'
        }
      }
    }, {
      contextValue: {
        user: { id: '1', roles: ['USER'] },
        db: mockDb,
        loaders: createLoaders(mockDb)
      }
    });
    
    expect(result.body.kind).toBe('single');
    expect(result.body.singleResult.data.createPost.title).toBe('Test Post');
  });
});
```

## Additional Resources

- See `graphql-best-practices.md` for comprehensive guidelines
- See `query-optimization.md` for performance patterns
- See `schema-design-patterns.md` for schema design
- See `../templates/resolver-examples.ts` for complete examples
