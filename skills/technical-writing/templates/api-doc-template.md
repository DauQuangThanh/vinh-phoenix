# API Documentation Template

## API Overview

Brief description of what this API does and its main purpose.

**Base URL:** `https://api.example.com/v1`

**Version:** 1.0.0

**Last Updated:** 2026-01-29

## Table of Contents

- [Authentication](#authentication)
- [Rate Limiting](#rate-limiting)
- [Errors](#errors)
- [Endpoints](#endpoints)
  - [Resource Name](#resource-name)
- [Webhooks](#webhooks)
- [SDKs](#sdks)
- [Changelog](#changelog)

## Authentication

### API Key Authentication

All API requests require authentication using an API key in the request header.

**Header Format:**

```http
Authorization: Bearer YOUR_API_KEY
```

**Example Request:**

```bash
curl -X GET https://api.example.com/v1/resource \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json"
```

### Getting an API Key

1. Sign up at [example.com](https://example.com)
2. Navigate to Settings > API Keys
3. Click "Generate New Key"
4. Copy and securely store your key

⚠️ **Security Note:** Never expose your API key in client-side code or public repositories.

### OAuth 2.0 (Optional)

For user-specific actions, use OAuth 2.0 authentication.

**Authorization URL:**

```
https://api.example.com/oauth/authorize?
  client_id=YOUR_CLIENT_ID&
  redirect_uri=YOUR_REDIRECT_URI&
  response_type=code&
  scope=read:user,write:user
```

**Token Exchange:**

```bash
curl -X POST https://api.example.com/oauth/token \
  -H "Content-Type: application/json" \
  -d '{
    "client_id": "YOUR_CLIENT_ID",
    "client_secret": "YOUR_CLIENT_SECRET",
    "code": "AUTHORIZATION_CODE",
    "grant_type": "authorization_code"
  }'
```

## Rate Limiting

Rate limits protect API availability:

**Limits:**

- **Free tier:** 100 requests/hour
- **Pro tier:** 1,000 requests/hour
- **Enterprise:** Custom limits

**Response Headers:**

```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1643648400
```

**429 Response (Rate Limit Exceeded):**

```json
{
  "error": "rate_limit_exceeded",
  "message": "API rate limit exceeded",
  "retry_after": 3600
}
```

**Best Practices:**

- Cache responses when possible
- Implement exponential backoff
- Monitor rate limit headers
- Upgrade plan if needed

## Errors

The API uses standard HTTP status codes and returns error details in JSON format.

### HTTP Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request succeeded |
| 201 | Created | Resource created successfully |
| 204 | No Content | Success with no response body |
| 400 | Bad Request | Invalid request parameters |
| 401 | Unauthorized | Missing or invalid authentication |
| 403 | Forbidden | Authenticated but not authorized |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | Resource conflict (e.g., duplicate) |
| 422 | Unprocessable Entity | Validation error |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Server error |
| 503 | Service Unavailable | Temporary service interruption |

### Error Response Format

```json
{
  "error": "error_code",
  "message": "Human-readable error message",
  "details": {
    "field": "specific_field",
    "reason": "Additional context"
  },
  "request_id": "req_abc123",
  "documentation_url": "https://docs.example.com/errors/error_code"
}
```

### Common Errors

#### Authentication Errors

**401 Unauthorized - Missing API Key:**

```json
{
  "error": "unauthorized",
  "message": "Missing or invalid API key",
  "documentation_url": "https://docs.example.com/authentication"
}
```

**403 Forbidden - Insufficient Permissions:**

```json
{
  "error": "forbidden",
  "message": "Insufficient permissions to access this resource"
}
```

#### Validation Errors

**400 Bad Request:**

```json
{
  "error": "validation_error",
  "message": "Request validation failed",
  "details": {
    "email": "Invalid email format",
    "age": "Must be a positive integer"
  }
}
```

## Endpoints

### Resource Name

Description of this resource group.

---

#### Create Resource

Create a new resource.

**Endpoint:**

```http
POST /v1/resources
```

**Authentication:** Required

**Request Headers:**

```http
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json
```

**Request Body:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | string | Yes | Resource name (2-100 characters) |
| `description` | string | No | Resource description (max 500 characters) |
| `type` | string | Yes | Resource type. Options: `type1`, `type2`, `type3` |
| `metadata` | object | No | Additional metadata |
| `tags` | array[string] | No | Array of tags (max 10) |

**Example Request:**

```bash
curl -X POST https://api.example.com/v1/resources \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Resource",
    "description": "A test resource",
    "type": "type1",
    "metadata": {
      "custom_field": "value"
    },
    "tags": ["production", "v1"]
  }'
```

**Success Response (201 Created):**

```json
{
  "id": "res_abc123",
  "name": "My Resource",
  "description": "A test resource",
  "type": "type1",
  "status": "active",
  "metadata": {
    "custom_field": "value"
  },
  "tags": ["production", "v1"],
  "created_at": "2026-01-29T10:30:00Z",
  "updated_at": "2026-01-29T10:30:00Z"
}
```

**Error Responses:**

**400 Bad Request - Validation Error:**

```json
{
  "error": "validation_error",
  "message": "Invalid request parameters",
  "details": {
    "name": "Name is required",
    "type": "Invalid type value"
  }
}
```

**409 Conflict - Duplicate Resource:**

```json
{
  "error": "duplicate_resource",
  "message": "A resource with this name already exists",
  "existing_resource_id": "res_xyz789"
}
```

---

#### Get Resource

Retrieve a specific resource by ID.

**Endpoint:**

```http
GET /v1/resources/{id}
```

**Authentication:** Required

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | string | Resource ID (format: `res_*`) |

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `include` | string | No | Related data to include. Options: `metadata`, `stats`, `all` |

**Example Request:**

```bash
curl -X GET "https://api.example.com/v1/resources/res_abc123?include=metadata" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**Success Response (200 OK):**

```json
{
  "id": "res_abc123",
  "name": "My Resource",
  "description": "A test resource",
  "type": "type1",
  "status": "active",
  "metadata": {
    "custom_field": "value"
  },
  "tags": ["production", "v1"],
  "created_at": "2026-01-29T10:30:00Z",
  "updated_at": "2026-01-29T10:30:00Z"
}
```

**Error Response:**

**404 Not Found:**

```json
{
  "error": "not_found",
  "message": "Resource not found",
  "resource_id": "res_abc123"
}
```

---

#### List Resources

Retrieve a paginated list of resources.

**Endpoint:**

```http
GET /v1/resources
```

**Authentication:** Required

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `page` | integer | No | 1 | Page number (min: 1) |
| `limit` | integer | No | 50 | Items per page (min: 1, max: 100) |
| `type` | string | No | - | Filter by type |
| `status` | string | No | - | Filter by status: `active`, `inactive`, `archived` |
| `search` | string | No | - | Search in name and description |
| `sort` | string | No | `created_at` | Sort field: `created_at`, `updated_at`, `name` |
| `order` | string | No | `desc` | Sort order: `asc`, `desc` |

**Example Request:**

```bash
curl -X GET "https://api.example.com/v1/resources?page=1&limit=10&type=type1&sort=name&order=asc" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**Success Response (200 OK):**

```json
{
  "data": [
    {
      "id": "res_abc123",
      "name": "My Resource",
      "type": "type1",
      "status": "active",
      "created_at": "2026-01-29T10:30:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total_items": 42,
    "total_pages": 5,
    "has_next": true,
    "has_previous": false
  }
}
```

---

#### Update Resource

Update an existing resource.

**Endpoint:**

```http
PATCH /v1/resources/{id}
```

**Authentication:** Required

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | string | Resource ID |

**Request Body:**

Only include fields you want to update.

| Parameter | Type | Description |
|-----------|------|-------------|
| `name` | string | Resource name |
| `description` | string | Resource description |
| `status` | string | Resource status: `active`, `inactive`, `archived` |
| `tags` | array[string] | Array of tags |

**Example Request:**

```bash
curl -X PATCH https://api.example.com/v1/resources/res_abc123 \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Resource Name",
    "status": "inactive"
  }'
```

**Success Response (200 OK):**

```json
{
  "id": "res_abc123",
  "name": "Updated Resource Name",
  "description": "A test resource",
  "type": "type1",
  "status": "inactive",
  "updated_at": "2026-01-29T11:00:00Z"
}
```

---

#### Delete Resource

Delete a resource permanently.

**Endpoint:**

```http
DELETE /v1/resources/{id}
```

**Authentication:** Required

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | string | Resource ID |

**Example Request:**

```bash
curl -X DELETE https://api.example.com/v1/resources/res_abc123 \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**Success Response (204 No Content):**

No response body.

**Error Response:**

**404 Not Found:**

```json
{
  "error": "not_found",
  "message": "Resource not found"
}
```

---

## Pagination

All list endpoints use cursor-based or page-based pagination.

**Response Format:**

```json
{
  "data": [...],
  "pagination": {
    "page": 1,
    "limit": 50,
    "total_items": 150,
    "total_pages": 3,
    "has_next": true,
    "has_previous": false
  }
}
```

**Navigating Pages:**

```bash
# Page 1
GET /v1/resources?page=1&limit=50

# Page 2
GET /v1/resources?page=2&limit=50
```

## Webhooks

Receive real-time notifications for events.

### Webhook Events

| Event | Description |
|-------|-------------|
| `resource.created` | Resource was created |
| `resource.updated` | Resource was updated |
| `resource.deleted` | Resource was deleted |

### Webhook Payload

```json
{
  "event": "resource.created",
  "data": {
    "id": "res_abc123",
    "name": "My Resource"
  },
  "timestamp": "2026-01-29T10:30:00Z",
  "webhook_id": "whk_xyz789"
}
```

### Webhook Signature

Verify webhook authenticity using the signature header:

```javascript
const crypto = require('crypto');

function verifyWebhook(payload, signature, secret) {
  const hmac = crypto.createHmac('sha256', secret);
  const digest = hmac.update(payload).digest('hex');
  return crypto.timingSafeEqual(
    Buffer.from(signature),
    Buffer.from(digest)
  );
}
```

## SDKs

Official SDKs available:

### JavaScript/TypeScript

```bash
npm install @example/api-client
```

```javascript
const { ExampleAPI } = require('@example/api-client');

const client = new ExampleAPI({ apiKey: 'YOUR_API_KEY' });
const resource = await client.resources.create({ name: 'My Resource' });
```

### Python

```bash
pip install example-api
```

```python
from example_api import ExampleAPI

client = ExampleAPI(api_key='YOUR_API_KEY')
resource = client.resources.create(name='My Resource')
```

### Other SDKs

- Ruby: [example-ruby](https://github.com/example/example-ruby)
- Go: [example-go](https://github.com/example/example-go)
- PHP: [example-php](https://github.com/example/example-php)

## Changelog

### v1.0.0 (2026-01-29)

- Initial API release
- Added resource CRUD endpoints
- Added authentication support

---

**Need Help?**

- [API Documentation](https://docs.example.com)
- [Support](https://support.example.com)
- [Status Page](https://status.example.com)
