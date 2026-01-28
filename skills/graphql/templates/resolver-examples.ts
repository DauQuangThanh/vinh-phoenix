// TypeScript Resolver Examples for GraphQL

import { GraphQLResolveInfo } from 'graphql';
import DataLoader from 'dataloader';

// Types
interface Context {
  user: User | null;
  loaders: {
    user: DataLoader<string, User>;
    post: DataLoader<string, Post>;
  };
  db: Database;
}

interface User {
  id: string;
  username: string;
  email: string;
  displayName: string;
}

interface Post {
  id: string;
  content: string;
  authorId: string;
  createdAt: Date;
}

// Resolvers
const resolvers = {
  Query: {
    // Get current user
    me: (parent: any, args: any, context: Context) => {
      if (!context.user) {
        throw new Error('Not authenticated');
      }
      return context.user;
    },

    // Get user by username
    user: async (
      parent: any,
      { username }: { username: string },
      context: Context
    ) => {
      const user = await context.db.users.findUnique({
        where: { username }
      });

      if (!user) {
        throw new Error('User not found');
      }

      return user;
    },

    // Get post by ID
    post: async (
      parent: any,
      { id }: { id: string },
      context: Context
    ) => {
      return context.loaders.post.load(id);
    },

    // Get personalized feed with pagination
    feed: async (
      parent: any,
      { first = 20, after }: { first?: number; after?: string },
      context: Context
    ) => {
      if (!context.user) {
        throw new Error('Not authenticated');
      }

      const offset = after ? parseInt(decodeCursor(after)) : 0;

      // Get posts from followed users
      const following = await context.db.follows.findMany({
        where: { followerId: context.user.id }
      });

      const followingIds = following.map(f => f.followingId);

      // Fetch posts (one extra to check if there's more)
      const posts = await context.db.posts.findMany({
        where: {
          authorId: { in: followingIds }
        },
        orderBy: { createdAt: 'desc' },
        skip: offset,
        take: first + 1
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
          hasPreviousPage: offset > 0,
          startCursor: edges[0]?.cursor || null,
          endCursor: edges[edges.length - 1]?.cursor || null
        },
        totalCount: await context.db.posts.count({
          where: { authorId: { in: followingIds } }
        })
      };
    }
  },

  Mutation: {
    // Create user
    createUser: async (
      parent: any,
      { input }: { input: CreateUserInput },
      context: Context
    ) => {
      // Validate input
      const errors = validateUserInput(input);
      if (errors.length > 0) {
        return { user: null, token: null, errors };
      }

      // Check if username exists
      const existing = await context.db.users.findUnique({
        where: { username: input.username }
      });

      if (existing) {
        return {
          user: null,
          token: null,
          errors: [{
            field: 'username',
            message: 'Username already taken',
            code: 'DUPLICATE_USERNAME'
          }]
        };
      }

      // Hash password
      const hashedPassword = await hashPassword(input.password);

      // Create user
      const user = await context.db.users.create({
        data: {
          username: input.username,
          email: input.email,
          password: hashedPassword,
          displayName: input.displayName
        }
      });

      // Generate token
      const token = generateJWT(user.id);

      return { user, token, errors: [] };
    },

    // Create post
    createPost: async (
      parent: any,
      { input }: { input: CreatePostInput },
      context: Context
    ) => {
      if (!context.user) {
        return {
          post: null,
          errors: [{
            field: null,
            message: 'Authentication required',
            code: 'UNAUTHENTICATED'
          }]
        };
      }

      // Validate content
      if (input.content.length === 0) {
        return {
          post: null,
          errors: [{
            field: 'content',
            message: 'Content cannot be empty',
            code: 'VALIDATION_ERROR'
          }]
        };
      }

      if (input.content.length > 5000) {
        return {
          post: null,
          errors: [{
            field: 'content',
            message: 'Content too long (max 5000 characters)',
            code: 'VALIDATION_ERROR'
          }]
        };
      }

      // Create post
      const post = await context.db.posts.create({
        data: {
          content: input.content,
          images: input.images || [],
          videoUrl: input.videoUrl,
          authorId: context.user.id
        }
      });

      return { post, errors: [] };
    },

    // Like post
    likePost: async (
      parent: any,
      { postId }: { postId: string },
      context: Context
    ) => {
      if (!context.user) {
        throw new Error('Authentication required');
      }

      // Check if post exists
      const post = await context.loaders.post.load(postId);
      if (!post) {
        throw new Error('Post not found');
      }

      // Check if already liked
      const existing = await context.db.likes.findUnique({
        where: {
          userId_postId: {
            userId: context.user.id,
            postId
          }
        }
      });

      if (existing) {
        return post; // Already liked
      }

      // Create like
      await context.db.likes.create({
        data: {
          userId: context.user.id,
          postId
        }
      });

      // Invalidate cache
      context.loaders.post.clear(postId);

      // Return updated post
      return context.loaders.post.load(postId);
    },

    // Follow user
    followUser: async (
      parent: any,
      { userId }: { userId: string },
      context: Context
    ) => {
      if (!context.user) {
        throw new Error('Authentication required');
      }

      if (userId === context.user.id) {
        throw new Error('Cannot follow yourself');
      }

      // Check if user exists
      const targetUser = await context.loaders.user.load(userId);
      if (!targetUser) {
        throw new Error('User not found');
      }

      // Check if already following
      const existing = await context.db.follows.findUnique({
        where: {
          followerId_followingId: {
            followerId: context.user.id,
            followingId: userId
          }
        }
      });

      if (existing) {
        return targetUser; // Already following
      }

      // Create follow relationship
      await context.db.follows.create({
        data: {
          followerId: context.user.id,
          followingId: userId
        }
      });

      // Invalidate cache
      context.loaders.user.clear(userId);

      return context.loaders.user.load(userId);
    }
  },

  // Type resolvers
  User: {
    // Resolve posts for a user
    posts: async (
      user: User,
      { first = 10, after }: { first?: number; after?: string },
      context: Context
    ) => {
      const offset = after ? parseInt(decodeCursor(after)) : 0;

      const posts = await context.db.posts.findMany({
        where: { authorId: user.id },
        orderBy: { createdAt: 'desc' },
        skip: offset,
        take: first + 1
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
          hasPreviousPage: offset > 0,
          startCursor: edges[0]?.cursor || null,
          endCursor: edges[edges.length - 1]?.cursor || null
        }
      };
    },

    // Resolve followers count
    followersCount: async (user: User, args: any, context: Context) => {
      return context.db.follows.count({
        where: { followingId: user.id }
      });
    },

    // Resolve if current user follows this user
    isFollowedByMe: async (user: User, args: any, context: Context) => {
      if (!context.user) return false;

      const follow = await context.db.follows.findUnique({
        where: {
          followerId_followingId: {
            followerId: context.user.id,
            followingId: user.id
          }
        }
      });

      return !!follow;
    }
  },

  Post: {
    // Resolve author using DataLoader
    author: (post: Post, args: any, context: Context) => {
      return context.loaders.user.load(post.authorId);
    },

    // Resolve likes count
    likesCount: async (post: Post, args: any, context: Context) => {
      return context.db.likes.count({
        where: { postId: post.id }
      });
    },

    // Resolve if current user liked this post
    isLikedByMe: async (post: Post, args: any, context: Context) => {
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
    },

    // Resolve comments with pagination
    comments: async (
      post: Post,
      { first = 10, after }: { first?: number; after?: string },
      context: Context
    ) => {
      const offset = after ? parseInt(decodeCursor(after)) : 0;

      const comments = await context.db.comments.findMany({
        where: { postId: post.id, parentId: null },
        orderBy: { createdAt: 'desc' },
        skip: offset,
        take: first + 1
      });

      const hasNextPage = comments.length > first;
      const edges = comments.slice(0, first).map((comment, index) => ({
        node: comment,
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

// Helper functions
function encodeCursor(offset: number): string {
  return Buffer.from(offset.toString()).toString('base64');
}

function decodeCursor(cursor: string): string {
  return Buffer.from(cursor, 'base64').toString('utf-8');
}

function validateUserInput(input: CreateUserInput): Error[] {
  const errors: Error[] = [];

  if (input.username.length < 3) {
    errors.push({
      field: 'username',
      message: 'Username must be at least 3 characters',
      code: 'VALIDATION_ERROR'
    });
  }

  if (!isValidEmail(input.email)) {
    errors.push({
      field: 'email',
      message: 'Invalid email format',
      code: 'VALIDATION_ERROR'
    });
  }

  if (input.password.length < 8) {
    errors.push({
      field: 'password',
      message: 'Password must be at least 8 characters',
      code: 'VALIDATION_ERROR'
    });
  }

  return errors;
}

function isValidEmail(email: string): boolean {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

async function hashPassword(password: string): Promise<string> {
  // Use bcrypt or similar
  return password; // Placeholder
}

function generateJWT(userId: string): string {
  // Generate JWT token
  return 'token'; // Placeholder
}

export default resolvers;
