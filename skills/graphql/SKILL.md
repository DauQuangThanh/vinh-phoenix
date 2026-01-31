---
name: graphql
description: Designs GraphQL schemas, writes queries and mutations, implements resolvers, and optimizes GraphQL APIs. Use when building GraphQL APIs, creating schemas, writing queries, implementing subscriptions, or when user mentions GraphQL, Apollo, schema design, queries, mutations, or API optimization.
metadata:
  author: Dau Quang Thanh
  version: "1.0.0"
  last-updated: "2026-01-28"
  categories: [api-development, backend, database]
license: MIT
---

# GraphQL Skill

## Overview

This skill provides comprehensive guidance for GraphQL API development, including schema design, query optimization, resolver implementation, and testing. It supports both server-side and client-side GraphQL development with best practices for performance, security, and maintainability.

## When to Use

- Designing GraphQL schemas from requirements
- Writing queries, mutations, and subscriptions
- Implementing resolvers with proper error handling
- Optimizing GraphQL queries and reducing over-fetching
- Setting up GraphQL servers (Apollo Server, GraphQL Yoga, etc.)
- Integrating GraphQL with databases and REST APIs
- Testing GraphQL APIs
- Migrating REST APIs to GraphQL
- Implementing authentication and authorization in GraphQL
- Schema validation and documentation

## Prerequisites

### Required Tools

- Node.js 18+ or Python 3.8+
- Package manager (npm, yarn, or pip)
- Code editor with GraphQL support

### Recommended Packages

**Node.js/TypeScript:**

- `graphql` - GraphQL.js reference implementation
- `@apollo/server` or `graphql-yoga` - GraphQL server frameworks
- `@graphql-tools/schema` - Schema building utilities
- `graphql-tag` - Query parsing
- `@graphql-codegen/cli` - Code generation

**Python:**

- `graphene` - GraphQL framework for Python
- `ariadne` - Schema-first GraphQL library
- `strawberry-graphql` - Code-first GraphQL library

## Instructions

### Step 1: Design the Schema

Follow schema-first or code-first approach based on project needs.

**Schema-First Approach:**

1. Define types in SDL (Schema Definition Language)
2. Define queries, mutations, and subscriptions
3. Document using descriptions
4. Validate schema structure

**Code-First Approach:**

1. Define types using decorators or classes
2. Generate SDL automatically from code
3. Ensure type safety with TypeScript/Python types

**Best Practices:**

- Use meaningful, consistent naming (PascalCase for types, camelCase for fields)
- Design around business domain, not database structure
- Keep types focused and cohesive
- Use interfaces for shared fields
- Implement proper pagination (cursor-based recommended)
- Version through field deprecation, not breaking changes

See `references/schema-design-patterns.md` for detailed patterns.

### Step 2: Implement Resolvers

Create efficient resolvers with proper data loading and error handling.

**Key Principles:**

- Implement DataLoader to prevent N+1 queries
- Use context for shared resources (database, auth)
- Validate inputs and check authorization in mutations
- Handle errors consistently with proper codes
- Return meaningful error messages

**Basic Pattern:**

```typescript
const resolvers = {
  Query: { user: (parent, { id }, ctx) => ctx.loaders.user.load(id) },
  Mutation: { createUser: async (parent, { input }, ctx) => {
    // Validate, authorize, then create
    return ctx.db.users.create({ data: input });
  }},
  User: { posts: (user, args, ctx) => ctx.loaders.postsByUser.load(user.id) }
};
```

See `references/resolver-implementation.md` for complete patterns, DataLoader setup, and authentication examples.

### Step 3: Optimize Queries

Prevent performance issues through proper query optimization.

**Common Optimizations:**

1. **Use DataLoader for batching:**
   - Batch multiple requests into single query
   - Cache within single request lifecycle

2. **Implement depth limiting:**
   - Prevent deeply nested queries
   - Set maximum query depth (typically 5-7)

3. **Query complexity analysis:**
   - Assign cost to each field
   - Reject queries exceeding threshold

4. **Pagination:**
   - Use cursor-based pagination for large datasets
   - Implement proper connection pattern

5. **Field-level caching:**
   - Cache expensive computations
   - Use appropriate TTL values

See `references/query-optimization.md` for implementation details.

### Step 4: Implement Authentication & Authorization

Secure GraphQL APIs with proper auth patterns.

**Authentication:** Validate JWT tokens in context and set user object
**Authorization:** Check permissions in resolvers or use directives

**Quick Example:**

```typescript
context: async ({ req }) => {
  const token = req.headers.authorization?.replace('Bearer ', '');
  const user = await validateToken(token);
  return { user, db, loaders: createLoaders(db) };
}

// In resolver
if (!context.user?.hasRole('admin')) throw new Error('Unauthorized');
```

See `references/resolver-implementation.md` for directive-based auth and field-level permissions.

### Step 5: Write and Test Queries

Create efficient, maintainable queries.

**Query Best Practices:**

- Request only needed fields
- Use fragments for reusable field sets
- Implement proper error handling
- Use variables instead of inline values
- Name all operations

**Testing:**

- Test resolvers in isolation
- Test complete queries end-to-end
- Test error scenarios
- Test authorization rules
- Use GraphQL query testing tools

Use `scripts/test-query.py` for automated query testing.

### Step 6: Generate Documentation

Maintain comprehensive API documentation.

**Documentation Strategies:**

- Add descriptions to all types and fields
- Document expected input formats
- Explain error scenarios
- Provide usage examples
- Keep schema and docs in sync

**Tools:**

- GraphQL Playground / GraphiQL for interactive docs
- GraphQL Voyager for schema visualization
- Custom documentation generators

### Step 7: Monitor and Debug

Implement observability for production GraphQL APIs.

**Monitoring:**

- Track query execution time
- Monitor resolver performance
- Log slow queries
- Track error rates
- Monitor cache hit rates

**Debugging:**

- Use Apollo Studio or similar tools
- Enable detailed error messages in development
- Sanitize errors in production
- Implement structured logging
- Use tracing for performance analysis

## Examples

### Example 1: Complete Schema Definition

```graphql
"""
User account in the system
"""
type User {
  id: ID!
  email: String!
  name: String!
  posts(first: Int, after: String): PostConnection!
  createdAt: DateTime!
}

"""
Blog post created by users
"""
type Post {
  id: ID!
  title: String!
  content: String!
  author: User!
  published: Boolean!
  tags: [String!]!
  createdAt: DateTime!
  updatedAt: DateTime!
}

"""
Paginated post results
"""
type PostConnection {
  edges: [PostEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}

type PostEdge {
  node: Post!
  cursor: String!
}

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}

input CreatePostInput {
  title: String!
  content: String!
  tags: [String!]
}

type Query {
  user(id: ID!): User
  post(id: ID!): Post
  posts(first: Int, after: String): PostConnection!
}

type Mutation {
  createPost(input: CreatePostInput!): Post!
  updatePost(id: ID!, input: CreatePostInput!): Post!
  deletePost(id: ID!): Boolean!
}

type Subscription {
  postCreated: Post!
}

scalar DateTime
```

### Example 2: Efficient Query with Fragments

```graphql
fragment UserBasic on User {
  id
  name
  email
}

fragment PostSummary on Post {
  id
  title
  published
  createdAt
  author {
    ...UserBasic
  }
}

query GetUserWithPosts($userId: ID!, $first: Int = 10) {
  user(id: $userId) {
    ...UserBasic
    posts(first: $first) {
      edges {
        node {
          ...PostSummary
        }
      }
      pageInfo {
        hasNextPage
        endCursor
      }
    }
  }
}
```

### Example 3: DataLoader Usage

```typescript
// Create loader
const userLoader = new DataLoader(async (ids) => {
  const users = await db.users.findMany({ where: { id: { in: ids } } });
  const map = new Map(users.map(u => [u.id, u]));
  return ids.map(id => map.get(id) || null);
});

// Use in resolver
Post: { author: (post, args, { loaders }) => loaders.user.load(post.authorId) }
```

See `references/resolver-implementation.md` for complete DataLoader patterns.

## Edge Cases

### Circular References

- GraphQL handles circular types naturally
- Implement query depth limiting (5-7 levels) to prevent abuse

### Large Result Sets

- Always implement pagination with reasonable defaults (10-100)
- Use cursor-based pagination for consistency

### N+1 Query Problem

- Use DataLoader for all relationship fields
- Monitor query counts in development

### Schema Evolution

- Use `@deprecated` directive instead of removing fields
- Add new fields rather than changing existing ones

### Complex Validation

- Use input validation libraries (Zod, Yup)
- Return detailed error messages with field-level feedback

See `references/resolver-implementation.md` for detailed handling patterns.

## Error Handling

Use standard error codes with GraphQLError:

```typescript
import { GraphQLError } from 'graphql';

// Validation error
throw new GraphQLError('Invalid email format', {
  extensions: { code: 'VALIDATION_ERROR', field: 'email' }
});

// Authentication
throw new GraphQLError('Authentication required', {
  extensions: { code: 'UNAUTHENTICATED' }
});

// Authorization
throw new GraphQLError('Insufficient permissions', {
  extensions: { code: 'FORBIDDEN', requiredRole: 'admin' }
});

// Not found
throw new GraphQLError(`User ${id} not found`, {
  extensions: { code: 'NOT_FOUND', resource: 'User', id }
});
```

See `references/resolver-implementation.md` for error handling patterns and validation with Zod.

## Scripts

### Validate GraphQL Schema

Validates schema syntax and structure:

```bash
python scripts/validate-schema.py path/to/schema.graphql
```

### Test GraphQL Query

Tests queries against a GraphQL endpoint:

```bash
python scripts/test-query.py --endpoint http://localhost:4000/graphql \
  --query-file queries/get-user.graphql \
  --variables '{"id": "123"}'
```

### Generate Schema Documentation

Generates markdown documentation from schema:

```bash
python scripts/generate-docs.py --schema schema.graphql --output docs/api.md
```

## Guidelines

1. **Always use meaningful names** - Types, fields, and arguments should clearly indicate their purpose
2. **Implement proper pagination** - Never return unbounded lists
3. **Use DataLoader** - Prevent N+1 queries in all relationship resolvers
4. **Validate inputs** - Check all mutation inputs before processing
5. **Handle errors gracefully** - Return specific, actionable error messages
6. **Document thoroughly** - Add descriptions to all schema elements
7. **Think in graphs** - Design around relationships, not CRUD operations
8. **Security first** - Implement authentication, authorization, and rate limiting
9. **Monitor performance** - Track query execution times and optimize slow queries
10. **Version carefully** - Use deprecation instead of breaking changes

## Additional Resources

- See `references/schema-design-patterns.md` for common schema patterns
- See `references/query-optimization.md` for performance best practices
- See `references/graphql-best-practices.md` for comprehensive guidelines
- See `templates/` for starter schemas and queries
- Official GraphQL documentation: <https://graphql.org/learn/>
- Apollo Server documentation: <https://www.apollographql.com/docs/apollo-server/>
