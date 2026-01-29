# Complete Documentation Examples

This reference provides complete, real-world examples of different documentation types to guide your technical writing.

## Example 1: README File for a Library

**Input:** Create README for a Python logging library called "LogMaster"

**Output:**

```markdown
# LogMaster

A flexible and powerful logging library for Python applications with built-in structured logging and multiple output formats.

## Features

- 📝 Structured logging with JSON output
- 🎨 Colored console output
- 📁 File rotation and compression
- 🔍 Log filtering and search
- 🔌 Plugin system for custom handlers

## Installation

```bash
pip install logmaster
```

## Quick Start

```python
from logmaster import Logger

# Create logger instance
logger = Logger("myapp")

# Log messages
logger.info("Application started")
logger.error("An error occurred", extra={"user_id": 123})
```

## Configuration

```python
from logmaster import Logger, Config

config = Config(
    level="INFO",
    format="json",
    output="./logs/app.log",
    rotation="daily"
)

logger = Logger("myapp", config=config)
```

## Documentation

Full documentation available at [docs.logmaster.io](https://docs.logmaster.io)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License - see [LICENSE](LICENSE)

```

## Example 2: API Endpoint Documentation

**Input:** Document a REST API endpoint for user creation

**Output:**

```markdown
## Create User

Creates a new user account.

### Endpoint

```http
POST /api/v1/users
```

### Authentication

Requires API key in header:

```http
Authorization: Bearer YOUR_API_KEY
```

### Request Body

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| email | string | Yes | User email address |
| name | string | Yes | User full name |
| role | string | No | User role (default: "user") |

### Example Request

```bash
curl -X POST https://api.example.com/api/v1/users \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "name": "John Doe",
    "role": "admin"
  }'
```

### Success Response

**Code:** `201 Created`

```json
{
  "id": "usr_abc123",
  "email": "user@example.com",
  "name": "John Doe",
  "role": "admin",
  "created_at": "2026-01-29T10:30:00Z"
}
```

### Error Responses

**Code:** `400 Bad Request`

```json
{
  "error": "validation_error",
  "message": "Invalid email format"
}
```

**Code:** `409 Conflict`

```json
{
  "error": "duplicate_email",
  "message": "User with this email already exists"
}
```

**Code:** `401 Unauthorized`

```json
{
  "error": "unauthorized",
  "message": "Invalid or missing API key"
}
```

### Rate Limiting

- 100 requests per hour per API key
- Rate limit headers included in response

```

## Example 3: Tutorial Document

**Input:** Create a tutorial for authentication setup

**Output:**

```markdown
# Setting Up Authentication

This tutorial walks you through implementing user authentication in your application using our Auth SDK.

**Time to complete:** 15 minutes
**Difficulty:** Intermediate

## Prerequisites

- Node.js 16+ installed
- Basic understanding of Express.js
- Auth SDK installed (`npm install @example/auth-sdk`)

## Step 1: Initialize the Auth Client

Create an auth client with your credentials:

```javascript
const { AuthClient } = require('@example/auth-sdk');

const authClient = new AuthClient({
  apiKey: process.env.AUTH_API_KEY,
  redirectUri: 'http://localhost:3000/callback'
});
```

💡 **Tip:** Store your API key in environment variables, never in code.

## Step 2: Create Login Route

Add a login route that redirects to the authentication page:

```javascript
app.get('/login', (req, res) => {
  const authUrl = authClient.getAuthorizationUrl({
    scope: ['read:user', 'write:user']
  });
  res.redirect(authUrl);
});
```

## Step 3: Handle Callback

Create a callback route to handle the authentication response:

```javascript
app.get('/callback', async (req, res) => {
  try {
    const { code } = req.query;
    const tokens = await authClient.exchangeCode(code);
    
    // Store tokens securely
    req.session.accessToken = tokens.accessToken;
    req.session.refreshToken = tokens.refreshToken;
    
    res.redirect('/dashboard');
  } catch (error) {
    console.error('Authentication error:', error);
    res.redirect('/login?error=auth_failed');
  }
});
```

## Step 4: Protect Routes

Add middleware to protect authenticated routes:

```javascript
const requireAuth = async (req, res, next) => {
  const token = req.session.accessToken;
  
  if (!token) {
    return res.redirect('/login');
  }
  
  try {
    const user = await authClient.verifyToken(token);
    req.user = user;
    next();
  } catch (error) {
    res.redirect('/login');
  }
};

app.get('/dashboard', requireAuth, (req, res) => {
  res.json({ user: req.user });
});
```

## Step 5: Test Your Implementation

1. Start your application:

   ```bash
   npm start
   ```

2. Navigate to `http://localhost:3000/login`

3. Complete the authentication flow

4. Verify you can access `/dashboard`

## Next Steps

- Implement Refresh Token Rotation
- Add Social Login Providers
- Configure Session Management

## Troubleshooting

**Issue:** Redirect loop after login

- Check that callback URL matches configuration
- Verify session storage is working

**Issue:** "Invalid token" error

- Check API key is correct
- Verify token hasn't expired

```

## Example 4: Error Documentation

**Input:** Document authentication errors

**Output:**

```markdown
## Authentication Errors

### Error: `AUTH_001 - Invalid Credentials`

**Description:** Occurs when username or password is incorrect.

**HTTP Status:** `401 Unauthorized`

**Response:**

```json
{
  "error": "AUTH_001",
  "message": "Invalid credentials",
  "details": "The username or password you entered is incorrect"
}
```

**Causes:**

- Incorrect username or password
- Account not yet activated
- Caps Lock enabled

**Resolution:**

1. Verify credentials are correct
2. Check for case sensitivity
3. Reset password if forgotten
4. Contact support if account locked

**Prevention:**

- Use secure password manager
- Enable "show password" option when typing
- Implement account recovery flow

### Error: `AUTH_002 - Token Expired`

**Description:** Occurs when the authentication token has expired.

**HTTP Status:** `401 Unauthorized`

**Response:**

```json
{
  "error": "AUTH_002",
  "message": "Token expired",
  "details": "Your session has expired. Please log in again."
}
```

**Causes:**

- Token lifetime exceeded (default: 1 hour)
- User inactive for extended period
- System time mismatch

**Resolution:**

1. Refresh the token using refresh token
2. Re-authenticate if refresh token also expired
3. Verify system time is correct

**Prevention:**

- Implement automatic token refresh
- Use longer-lived refresh tokens
- Warn users before expiration

```

## Example 5: Configuration Documentation

**Input:** Document application configuration options

**Output:**

```markdown
## Configuration Reference

### Environment Variables

#### `DATABASE_URL`

- **Type:** String
- **Required:** Yes
- **Format:** `postgresql://user:password@host:port/database`
- **Example:** `postgresql://admin:secret@localhost:5432/myapp`
- **Description:** PostgreSQL database connection string

#### `LOG_LEVEL`

- **Type:** String
- **Required:** No
- **Default:** `info`
- **Allowed Values:** `debug`, `info`, `warn`, `error`
- **Example:** `LOG_LEVEL=debug`
- **Description:** Controls application logging verbosity

#### `PORT`

- **Type:** Integer
- **Required:** No
- **Default:** `3000`
- **Range:** `1024-65535`
- **Example:** `PORT=8080`
- **Description:** Port number for the application server

### Configuration File (config.yaml)

```yaml
# Application settings
app:
  name: "MyApp"
  version: "1.0.0"
  environment: "production"

# Server configuration
server:
  host: "0.0.0.0"
  port: 3000
  timeout: 30

# Database settings
database:
  host: "localhost"
  port: 5432
  name: "myapp"
  pool_size: 10
  ssl: true

# Cache configuration
cache:
  enabled: true
  ttl: 3600
  provider: "redis"
  redis:
    host: "localhost"
    port: 6379
```

### Configuration Priority

Configuration is loaded in the following order (later sources override earlier):

1. Default values
2. Configuration file (`config.yaml`)
3. Environment variables
4. Command-line arguments

```

## Best Practices for Examples

### Make Examples Realistic

- Use realistic data and scenarios
- Include common edge cases
- Show real error messages
- Use actual command output

### Keep Examples Focused

- One concept per example
- Minimal boilerplate code
- Highlight the key concept
- Remove unnecessary details

### Make Examples Runnable

- Include all necessary imports
- Specify version requirements
- Provide sample data
- Show expected output

### Explain the Example

- Add inline comments for complex parts
- Describe what the example demonstrates
- Highlight important details
- Link to related concepts
