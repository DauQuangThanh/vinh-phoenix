# GraphQL Schema Design Patterns

This reference provides proven patterns for designing scalable, maintainable GraphQL schemas.

## Core Design Principles

### 1. Design Around Your Domain, Not Your Database

**❌ Bad: Database-Driven Design**

```graphql
type user_accounts {
  user_id: Int!
  email_addr: String!
  created_ts: String!
  user_profile_fk: Int
}
```

**✅ Good: Domain-Driven Design**

```graphql
type User {
  id: ID!
  email: String!
  createdAt: DateTime!
  profile: UserProfile
}
```

**Why:** GraphQL should expose your business domain, not implementation details.

### 2. Use Meaningful Names

- **Types:** PascalCase (`User`, `BlogPost`, `OrderStatus`)
- **Fields:** camelCase (`firstName`, `createdAt`, `isPublished`)
- **Arguments:** camelCase (`userId`, `first`, `after`)
- **Enums:** UPPER_SNAKE_CASE (`PENDING`, `IN_PROGRESS`, `COMPLETED`)

### 3. Make Illegal States Unrepresentable

**❌ Bad: Nullable Fields That Should Always Exist**

```graphql
type User {
  id: ID
  email: String
}
```

**✅ Good: Required Fields Are Non-Null**

```graphql
type User {
  id: ID!
  email: String!
  middleName: String  # Nullable because it's optional
}
```

## Common Schema Patterns

### Pattern 1: Relay-Style Pagination (Cursor-Based)

Most scalable pagination approach for large datasets.

```graphql
type Query {
  posts(
    first: Int
    after: String
    last: Int
    before: String
  ): PostConnection!
}

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

type Post {
  id: ID!
  title: String!
  content: String!
}
```

**Usage:**

```graphql
query GetPosts {
  posts(first: 10) {
    edges {
      node {
        id
        title
      }
      cursor
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}

# Next page
query GetNextPosts($after: String!) {
  posts(first: 10, after: $after) {
    edges {
      node {
        id
        title
      }
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
```

### Pattern 2: Node Interface for Global Object Identification

Allows fetching any object by global ID.

```graphql
interface Node {
  id: ID!
}

type User implements Node {
  id: ID!
  name: String!
  email: String!
}

type Post implements Node {
  id: ID!
  title: String!
  author: User!
}

type Query {
  node(id: ID!): Node
  nodes(ids: [ID!]!): [Node]!
}
```

**Usage:**

```graphql
query GetAnyObject {
  node(id: "dXNlcjoxMjM=") {
    id
    ... on User {
      name
      email
    }
    ... on Post {
      title
    }
  }
}
```

### Pattern 3: Input Types for Mutations

Keep mutations consistent and extensible.

```graphql
input CreateUserInput {
  email: String!
  name: String!
  password: String!
}

input UpdateUserInput {
  email: String
  name: String
  # password handled separately for security
}

type CreateUserPayload {
  user: User
  errors: [Error!]
}

type UpdateUserPayload {
  user: User
  errors: [Error!]
}

type Mutation {
  createUser(input: CreateUserInput!): CreateUserPayload!
  updateUser(id: ID!, input: UpdateUserInput!): UpdateUserPayload!
}
```

**Benefits:**

- Easy to add new fields without breaking API
- Clear grouping of related inputs
- Consistent mutation signature pattern

### Pattern 4: Error Handling with Unions

Type-safe error handling.

```graphql
type User {
  id: ID!
  email: String!
}

type ValidationError {
  field: String!
  message: String!
}

type NotFoundError {
  message: String!
  resourceType: String!
  resourceId: ID!
}

union CreateUserResult = User | ValidationError

type Mutation {
  createUser(input: CreateUserInput!): CreateUserResult!
}
```

**Usage:**

```graphql
mutation CreateUser($input: CreateUserInput!) {
  createUser(input: $input) {
    ... on User {
      id
      email
    }
    ... on ValidationError {
      field
      message
    }
  }
}
```

### Pattern 5: Interfaces for Polymorphic Types

Share common fields across types.

```graphql
interface Content {
  id: ID!
  title: String!
  author: User!
  createdAt: DateTime!
  updatedAt: DateTime!
}

type Article implements Content {
  id: ID!
  title: String!
  author: User!
  createdAt: DateTime!
  updatedAt: DateTime!
  body: String!
  tags: [String!]!
}

type Video implements Content {
  id: ID!
  title: String!
  author: User!
  createdAt: DateTime!
  updatedAt: DateTime!
  url: String!
  duration: Int!
}

type Query {
  feed: [Content!]!
}
```

**Usage:**

```graphql
query GetFeed {
  feed {
    id
    title
    author {
      name
    }
    ... on Article {
      body
      tags
    }
    ... on Video {
      url
      duration
    }
  }
}
```

### Pattern 6: Filtering with Input Objects

Structured, type-safe filtering.

```graphql
enum SortOrder {
  ASC
  DESC
}

input PostFilter {
  authorId: ID
  published: Boolean
  tags: [String!]
  createdAfter: DateTime
  createdBefore: DateTime
}

input PostSort {
  field: PostSortField!
  order: SortOrder!
}

enum PostSortField {
  CREATED_AT
  UPDATED_AT
  TITLE
}

type Query {
  posts(
    filter: PostFilter
    sort: PostSort
    first: Int
    after: String
  ): PostConnection!
}
```

**Usage:**

```graphql
query GetRecentPublished {
  posts(
    filter: {
      published: true
      createdAfter: "2026-01-01"
    }
    sort: {
      field: CREATED_AT
      order: DESC
    }
    first: 20
  ) {
    edges {
      node {
        title
      }
    }
  }
}
```

### Pattern 7: Extending Types with Field Arguments

Add flexibility without type proliferation.

```graphql
type User {
  id: ID!
  name: String!
  
  # Flexible date formatting
  createdAt(format: String = "ISO8601"): String!
  
  # Paginated relationships
  posts(
    first: Int
    after: String
    filter: PostFilter
  ): PostConnection!
  
  # Computed fields with options
  avatarUrl(size: Int = 100): String!
}
```

### Pattern 8: Subscription Patterns

Real-time updates with filters.

```graphql
type Subscription {
  # All posts
  postCreated: Post!
  
  # Filtered by author
  postCreatedByAuthor(authorId: ID!): Post!
  
  # Filtered by multiple criteria
  postUpdated(filter: PostFilter): Post!
  
  # Channel-based
  messageAdded(channelId: ID!): Message!
}
```

**Usage:**

```graphql
subscription WatchNewPosts($authorId: ID!) {
  postCreatedByAuthor(authorId: $authorId) {
    id
    title
    content
  }
}
```

## Anti-Patterns to Avoid

### ❌ Anti-Pattern 1: Exposing Implementation Details

```graphql
# Bad: Exposing database IDs and internal structure
type user_table {
  pk_id: Int!
  fk_profile_id: Int
  deleted_at: String
}
```

**Fix:** Use domain language:

```graphql
type User {
  id: ID!
  profile: UserProfile
  # Don't expose soft-delete implementation
}
```

### ❌ Anti-Pattern 2: Non-Null Arrays of Nullable Items

```graphql
# Bad: Confusing nullability
type User {
  friends: [User]!  # Array is non-null but items can be null?
}
```

**Fix:** Be explicit:

```graphql
type User {
  friends: [User!]!  # Non-null array of non-null users
  # or
  friends: [User!]   # Nullable array of non-null users
}
```

### ❌ Anti-Pattern 3: Boolean Trap in Arguments

```graphql
# Bad: What does true/false mean?
type Query {
  posts(published: Boolean): [Post!]!
}
```

**Fix:** Use enums for clarity:

```graphql
enum PostStatus {
  PUBLISHED
  DRAFT
  ARCHIVED
}

type Query {
  posts(status: PostStatus): [Post!]!
}
```

### ❌ Anti-Pattern 4: Mutations Returning Scalar Values

```graphql
# Bad: No way to return errors or related data
type Mutation {
  deletePost(id: ID!): Boolean!
}
```

**Fix:** Return payload type:

```graphql
type DeletePostPayload {
  success: Boolean!
  deletedPostId: ID
  errors: [Error!]
}

type Mutation {
  deletePost(id: ID!): DeletePostPayload!
}
```

### ❌ Anti-Pattern 5: Deeply Nested Queries Without Limits

```graphql
# Dangerous: Can cause performance issues
type User {
  friends: [User!]!  # Each friend has friends...
}
```

**Fix:** Add pagination and depth limits:

```graphql
type User {
  friends(first: Int = 10, after: String): UserConnection!
}

# Plus implement query depth limiting in resolver
```

## Versioning Strategies

### Strategy 1: Field Deprecation (Recommended)

```graphql
type User {
  id: ID!
  
  # Old field
  name: String! @deprecated(reason: "Use firstName and lastName instead")
  
  # New fields
  firstName: String!
  lastName: String!
}
```

### Strategy 2: Additive Changes Only

- Always add new fields, never remove
- Use optional arguments with defaults
- Add new types for new features

### Strategy 3: Separate Schemas (Last Resort)

Only when breaking changes are absolutely necessary:

- `/graphql/v1/`
- `/graphql/v2/`

## Performance Optimization Patterns

### Pattern 1: DataLoader for Batching

```typescript
// Create loaders
const userLoader = new DataLoader(async (userIds) => {
  const users = await db.users.findMany({
    where: { id: { in: userIds } }
  });
  return userIds.map(id => users.find(u => u.id === id));
});

// Use in resolvers
const resolvers = {
  Post: {
    author: (post, args, { loaders }) => {
      return loaders.user.load(post.authorId);
    }
  }
};
```

### Pattern 2: Field-Level Caching

```graphql
type Query {
  # Cache for 5 minutes
  stats: SiteStats! @cacheControl(maxAge: 300)
  
  # No caching
  currentUser: User @cacheControl(maxAge: 0)
}
```

### Pattern 3: Deferred Queries

```graphql
query GetPost($id: ID!) {
  post(id: $id) {
    id
    title
    ... @defer {
      comments {
        edges {
          node {
            content
          }
        }
      }
    }
  }
}
```

## Testing Schema Design

### Checklist

- [ ] All required fields are non-null
- [ ] All optional fields are nullable
- [ ] Pagination implemented for lists
- [ ] Input types used for mutations
- [ ] Errors handled gracefully
- [ ] Names follow conventions
- [ ] Descriptions added to all types and fields
- [ ] No implementation details exposed
- [ ] Depth limiting configured
- [ ] DataLoader implemented for relationships
- [ ] Authorization rules defined
- [ ] Schema validated and documented

## Additional Resources

- [GraphQL Best Practices](https://graphql.org/learn/best-practices/)
- [Relay Cursor Connections Specification](https://relay.dev/graphql/connections.htm)
- [Apollo Server Performance](https://www.apollographql.com/docs/apollo-server/performance/)
