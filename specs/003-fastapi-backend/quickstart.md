# Quickstart: Running the FastAPI Backend

**Feature**: Secure FastAPI Backend with JWT & PostgreSQL
**Date**: 2026-01-08
**Audience**: Developers implementing Phase II

---

## Prerequisites

- Python 3.11+
- PostgreSQL 12+ (or Neon Serverless account)
- UV package manager
- Valid BETTER_AUTH_SECRET (shared with frontend)

---

## Installation & Setup

### 1. Clone & Navigate

```bash
cd /path/to/todo-app-Phase2/backend
```

### 2. Create Environment File

```bash
cp .env.example .env
```

**Edit `.env`** with your secrets:

```env
# JWT & Auth
BETTER_AUTH_SECRET=your-shared-secret-key-here

# Database
DATABASE_URL=postgresql://user:password@host:5432/todo_db
# For Neon: postgresql://user:password@neon-host/todo_db

# Development
DEBUG=true
LOG_LEVEL=info
```

**⚠️ IMPORTANT**: Never commit `.env` to git; it's in `.gitignore`

### 3. Install Dependencies

```bash
uv sync
```

Installs:
- fastapi
- sqlmodel
- pydantic
- pyjwt
- asyncpg
- python-dotenv
- pytest, pytest-asyncio, httpx (dev dependencies)

### 4. Initialize Database

```bash
# Using SQLModel to create all tables
python -c "from main import create_db_and_tables; import asyncio; asyncio.run(create_db_and_tables())"
```

Or manually run SQL:

```sql
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    title VARCHAR(200) NOT NULL CHECK (length(title) > 0),
    description VARCHAR(1000),
    completed BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_task_user_id ON tasks(user_id);
CREATE INDEX idx_task_user_created ON tasks(user_id, created_at);
CREATE INDEX idx_task_user_completed ON tasks(user_id, completed);
```

---

## Running the Server

### Development Mode

```bash
uvicorn main:app --reload --port 8000
```

Output:

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started server process [12345]
```

### Production Mode (with gunicorn - future)

```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

### Accessing Swagger UI

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

---

## Testing Endpoints via cURL

### Generate a Test JWT

```bash
# Create a token manually (for testing)
python -c "
import jwt
import os
from datetime import datetime, timedelta

secret = os.getenv('BETTER_AUTH_SECRET')
user_id = 'test-user-123'
payload = {
    'user_id': user_id,
    'iat': datetime.utcnow(),
    'exp': datetime.utcnow() + timedelta(hours=24)
}
token = jwt.encode(payload, secret, algorithm='HS256')
print(f'Bearer {token}')
"
```

Store the token:

```bash
export AUTH_TOKEN="Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."  # Replace with actual token
```

### Test Endpoints

**Create a task**:

```bash
curl -X POST http://localhost:8000/api/tasks \
  -H "Authorization: $AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries", "description": "milk, eggs, bread"}'
```

Response (201 Created):

```json
{
  "id": 1,
  "user_id": "test-user-123",
  "title": "Buy groceries",
  "description": "milk, eggs, bread",
  "completed": false,
  "created_at": "2026-01-08T10:30:00Z",
  "updated_at": "2026-01-08T10:30:00Z"
}
```

**List tasks**:

```bash
curl -X GET http://localhost:8000/api/tasks \
  -H "Authorization: $AUTH_TOKEN"
```

**List pending tasks**:

```bash
curl -X GET "http://localhost:8000/api/tasks?status=pending" \
  -H "Authorization: $AUTH_TOKEN"
```

**Get specific task**:

```bash
curl -X GET http://localhost:8000/api/tasks/1 \
  -H "Authorization: $AUTH_TOKEN"
```

**Update task**:

```bash
curl -X PUT http://localhost:8000/api/tasks/1 \
  -H "Authorization: $AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries (ASAP)", "description": "milk, eggs, bread, butter"}'
```

**Toggle completion**:

```bash
curl -X PATCH http://localhost:8000/api/tasks/1/complete \
  -H "Authorization: $AUTH_TOKEN"
```

**Delete task**:

```bash
curl -X DELETE http://localhost:8000/api/tasks/1 \
  -H "Authorization: $AUTH_TOKEN"
```

Response (204 No Content): Empty body

---

## Running Tests

### Unit Tests

```bash
pytest tests/test_auth.py -v
```

Tests JWT validation, token extraction, error cases.

### Integration Tests

```bash
pytest tests/test_tasks.py -v
```

Tests full CRUD flows with authorization.

### All Tests

```bash
pytest -v --cov=. --cov-report=html
```

Generates coverage report in `htmlcov/index.html`.

### Async Test Setup

All tests use pytest-asyncio markers:

```python
@pytest.mark.asyncio
async def test_list_tasks(client, valid_jwt):
    response = await client.get("/api/tasks", headers={"Authorization": f"Bearer {valid_jwt}"})
    assert response.status_code == 200
```

---

## Common Errors & Troubleshooting

### Error: 401 Unauthorized - "Invalid authentication credentials"

**Cause**: Missing or invalid JWT token

**Solution**:
1. Verify `Authorization: Bearer <token>` header is present
2. Check token is not expired
3. Verify `BETTER_AUTH_SECRET` matches between frontend and backend
4. Test token generation: `python -c "import jwt; print(jwt.decode(...))"`

### Error: 422 Unprocessable Entity - "string too long"

**Cause**: Title exceeds 200 characters

**Solution**:
1. Check title length: `len("your title") <= 200`
2. Description max length is 1000 characters
3. Empty titles rejected (min_length=1)

### Error: 404 Not Found - "Task not found"

**Cause**: Task doesn't exist OR belongs to another user

**Solution**:
1. List tasks to verify it exists: `GET /api/tasks`
2. Verify you're using the correct task ID
3. Check you're authenticated as the task owner

### Error: Connection refused - "Cannot connect to PostgreSQL"

**Cause**: Database not running or URL incorrect

**Solution**:
1. Verify PostgreSQL is running: `psql -c "SELECT 1"`
2. Test connection: `DATABASE_URL=... python -c "from db import engine; import asyncio; asyncio.run(engine.connect())"`
3. For Neon: Verify credentials and network access

### Error: "BETTER_AUTH_SECRET not found"

**Cause**: Environment variable not set

**Solution**:
1. Create `.env` file with `BETTER_AUTH_SECRET=...`
2. Or export: `export BETTER_AUTH_SECRET="your-secret"`
3. Verify it's loaded: `python -c "import os; print(os.getenv('BETTER_AUTH_SECRET'))"`

---

## Frontend Integration

### 1. Configure Frontend API Client

**`frontend/lib/api.ts`** should be configured to:
1. Get JWT from localStorage (set by Better Auth)
2. Attach to `Authorization: Bearer <token>` header
3. Send requests to `http://localhost:8000/api/tasks`

**Example**:

```typescript
const apiRequest = async (endpoint: string, options = {}) => {
  const token = localStorage.getItem('todo_auth_token')
  const headers = {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json',
  }
  const response = await fetch(`http://localhost:8000${endpoint}`, {
    ...options,
    headers: { ...headers, ...options.headers },
  })
  return response.json()
}
```

### 2. Configure CORS

Backend (`main.py`) must allow frontend origin:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 3. Test Full Flow

1. Start backend: `uvicorn main:app --reload --port 8000`
2. Start frontend: `npm run dev` (port 3000)
3. Sign in via Better Auth UI
4. Create a task from the UI
5. Verify task appears in task list
6. Edit and mark complete
7. Delete task

---

## Next Steps

### After Implementation

1. **Run full integration test suite**: `pytest -v`
2. **Check code coverage**: `pytest --cov`
3. **Verify Swagger documentation**: http://localhost:8000/docs
4. **Test with frontend**: Sign in and perform CRUD operations
5. **Load test** (optional): `locust -f locustfile.py`

### Debugging

- **Enable SQL logging**: Add `echo=True` to create_engine()
- **View request/response logs**: Increase `LOG_LEVEL=debug`
- **Test token decode**: `jwt.decode(token, secret, algorithms=["HS256"])`

### Security Checklist

- [ ] BETTER_AUTH_SECRET is secure and unique (NOT "secret")
- [ ] .env file is in .gitignore (no secrets in git)
- [ ] CORS allows only trusted origins
- [ ] All endpoints require valid JWT
- [ ] User isolation verified (cross-user 404 test)
- [ ] No SQL injection (using SQLModel ORM)
- [ ] HTTPS enabled in production

---

## Documentation

- **API Reference**: [contracts/openapi.json](./contracts/openapi.json)
- **Data Model**: [data-model.md](./data-model.md)
- **Architecture**: [plan.md](./plan.md)
- **Research**: [research.md](./research.md)

---

**Status**: Ready for implementation via `/sp.implement` or `/sp.tasks`

