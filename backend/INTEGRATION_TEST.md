# Integration Testing Guide

Manual integration testing commands to verify the FastAPI backend is working correctly.

## Prerequisites

1. Start the backend server:
```bash
cd backend
uvicorn main:app --reload --port 8000
```

2. Set up test credentials. First, create a test JWT token. You can use an online JWT encoder or create one programmatically:

```python
import jwt
import json
from datetime import datetime, timedelta

# Using the same secret as in your .env
secret = "c88P3613ehwm7mGcQTm7dJ6tv0AiYjnS"  # From .env BETTER_AUTH_SECRET
payload = {
    "sub": "test-user-1",
    "iat": datetime.utcnow(),
    "exp": datetime.utcnow() + timedelta(hours=1)
}
token = jwt.encode(payload, secret, algorithm="HS256")
print(f"Token: {token}")
```

Or use this example tokens (valid with the default secret):
- User 1: Use the token generated above with `sub: test-user-1`
- User 2: Use a token with `sub: test-user-2`

## Test Cases

### 1. Health Check (No Auth Required)

```bash
curl -X GET http://localhost:8000/health
```

Expected response:
```json
{"status": "ok", "version": "0.1.0"}
```

### 2. Create Task (Auth Required)

```bash
# Replace TOKEN with actual JWT
TOKEN="your-jwt-token-here"

curl -X POST http://localhost:8000/api/tasks \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Buy groceries",
    "description": "Milk, bread, eggs"
  }'
```

Expected response (201 Created):
```json
{
  "id": 1,
  "user_id": "test-user-1",
  "title": "Buy groceries",
  "description": "Milk, bread, eggs",
  "completed": false,
  "created_at": "2026-01-05T12:00:00",
  "updated_at": "2026-01-05T12:00:00"
}
```

### 3. List Tasks

```bash
TOKEN="your-jwt-token-here"

curl -X GET "http://localhost:8000/api/tasks" \
  -H "Authorization: Bearer $TOKEN"
```

Expected response (200 OK):
```json
{
  "items": [
    {
      "id": 1,
      "user_id": "test-user-1",
      "title": "Buy groceries",
      "description": "Milk, bread, eggs",
      "completed": false,
      "created_at": "2026-01-05T12:00:00",
      "updated_at": "2026-01-05T12:00:00"
    }
  ]
}
```

### 4. List Tasks with Status Filter (Pending)

```bash
TOKEN="your-jwt-token-here"

curl -X GET "http://localhost:8000/api/tasks?status=pending" \
  -H "Authorization: Bearer $TOKEN"
```

### 5. List Tasks with Status Filter (Completed)

```bash
TOKEN="your-jwt-token-here"

curl -X GET "http://localhost:8000/api/tasks?status=completed" \
  -H "Authorization: Bearer $TOKEN"
```

### 6. Get Single Task

```bash
TOKEN="your-jwt-token-here"

curl -X GET http://localhost:8000/api/tasks/1 \
  -H "Authorization: Bearer $TOKEN"
```

Expected response (200 OK):
```json
{
  "id": 1,
  "user_id": "test-user-1",
  "title": "Buy groceries",
  "description": "Milk, bread, eggs",
  "completed": false,
  "created_at": "2026-01-05T12:00:00",
  "updated_at": "2026-01-05T12:00:00"
}
```

### 7. Update Task

```bash
TOKEN="your-jwt-token-here"

curl -X PUT http://localhost:8000/api/tasks/1 \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Buy groceries and cook dinner"
  }'
```

Expected response (200 OK):
```json
{
  "id": 1,
  "user_id": "test-user-1",
  "title": "Buy groceries and cook dinner",
  "description": "Milk, bread, eggs",
  "completed": false,
  "created_at": "2026-01-05T12:00:00",
  "updated_at": "2026-01-05T12:05:00"
}
```

### 8. Toggle Task Complete

```bash
TOKEN="your-jwt-token-here"

curl -X PATCH http://localhost:8000/api/tasks/1/complete \
  -H "Authorization: Bearer $TOKEN"
```

Expected response (200 OK):
```json
{
  "id": 1,
  "user_id": "test-user-1",
  "title": "Buy groceries and cook dinner",
  "description": "Milk, bread, eggs",
  "completed": true,
  "created_at": "2026-01-05T12:00:00",
  "updated_at": "2026-01-05T12:05:30"
}
```

### 9. Delete Task

```bash
TOKEN="your-jwt-token-here"

curl -X DELETE http://localhost:8000/api/tasks/1 \
  -H "Authorization: Bearer $TOKEN"
```

Expected response (204 No Content):
```
(empty body)
```

### 10. Error Cases

#### 10a. Missing Authorization Header (401)

```bash
curl -X GET http://localhost:8000/api/tasks
```

Expected response (403 Forbidden):
```json
{"detail": "Not authenticated"}
```

#### 10b. Invalid Token (401)

```bash
curl -X GET http://localhost:8000/api/tasks \
  -H "Authorization: Bearer invalid-token"
```

Expected response (401 Unauthorized):
```json
{"detail": "Invalid token"}
```

#### 10c. Task Not Found (404)

```bash
TOKEN="your-jwt-token-here"

curl -X GET http://localhost:8000/api/tasks/999 \
  -H "Authorization: Bearer $TOKEN"
```

Expected response (404 Not Found):
```json
{"detail": "Task not found"}
```

#### 10d. Invalid Title (422)

```bash
TOKEN="your-jwt-token-here"

curl -X POST http://localhost:8000/api/tasks \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": ""
  }'
```

Expected response (422 Unprocessable Entity):
```json
{"detail": [...]}
```

### 11. User Isolation Test

Create tasks for two different users and verify they cannot access each other's tasks:

```bash
# Create token for User 1
TOKEN_USER1="token-with-sub-user-1"

# Create token for User 2
TOKEN_USER2="token-with-sub-user-2"

# User 1: Create task
curl -X POST http://localhost:8000/api/tasks \
  -H "Authorization: Bearer $TOKEN_USER1" \
  -H "Content-Type: application/json" \
  -d '{"title": "User 1 Task"}'

# Returns task with ID 1, user_id: user-1

# User 2: Try to access User 1's task
curl -X GET http://localhost:8000/api/tasks/1 \
  -H "Authorization: Bearer $TOKEN_USER2"

# Should return 404 Not Found
```

## Swagger UI

You can also test all endpoints interactively using Swagger UI:

```
http://localhost:8000/docs
```

1. Click the "Authorize" button in the top-right
2. Enter: `Bearer <your-jwt-token>`
3. Use the "Try it out" button on each endpoint

## Automated Test Suite

Run the automated test suite:

```bash
cd backend
pytest tests/test_tasks.py -v
```

Or with coverage:

```bash
pytest tests/test_tasks.py --cov=backend --cov-report=html
```

## Performance Testing

Quick performance test to verify response times:

```bash
# Create a task
time curl -X POST http://localhost:8000/api/tasks \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Performance Test"}'

# Get a task
time curl -X GET http://localhost:8000/api/tasks/1 \
  -H "Authorization: Bearer $TOKEN"

# List tasks
time curl -X GET http://localhost:8000/api/tasks \
  -H "Authorization: Bearer $TOKEN"
```

Expected:
- JWT verification: < 10ms
- Create: < 200ms
- Retrieve: < 100ms
- List: < 150ms

## Troubleshooting

### "Connection refused to database"
- Ensure PostgreSQL is running
- Check DATABASE_URL is correct
- Verify credentials are correct

### "Invalid token"
- Verify JWT was created with the correct BETTER_AUTH_SECRET
- Check token has not expired
- Ensure "Bearer " prefix is included in Authorization header

### "Task not found"
- Verify task ID exists
- Verify task belongs to the authenticated user
- Check user_id from token matches the owner

## Notes

- All timestamps are UTC (ISO 8601 format)
- User IDs come from JWT 'sub' claim
- Data persists across server restarts if using real PostgreSQL
- In-memory database (SQLite) for tests doesn't persist
