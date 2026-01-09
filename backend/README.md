# Todo Backend API

Secure FastAPI backend for Phase II todo application with JWT authentication, PostgreSQL persistence, and complete user isolation.

## Features

- ✅ **6 RESTful Endpoints**: Create, read, update, complete, delete, and list tasks
- ✅ **JWT Authentication**: HS256 with BETTER_AUTH_SECRET
- ✅ **User Isolation**: Every query filtered by `user_id` from JWT
- ✅ **PostgreSQL**: Neon serverless database with async connections
- ✅ **Async/Await**: Production-ready async patterns with asyncpg
- ✅ **Swagger Documentation**: Auto-generated OpenAPI docs at `/docs`
- ✅ **Status Filtering**: Filter tasks by pending/completed/all
- ✅ **Timestamps**: Auto-managed created_at and updated_at

## Setup

### Prerequisites
- Python 3.10+
- PostgreSQL account (Neon)

### Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create `.env` file:
```bash
cp .env.example .env
```

3. Run server:
```bash
uvicorn src.main:app --reload --port 8000
```

## API Endpoints

All endpoints require `Authorization: Bearer <JWT_TOKEN>` header.

- `POST /api/tasks` - Create task (201)
- `GET /api/tasks` - List tasks (200)
- `GET /api/tasks/{id}` - Get task detail (200/404)
- `PUT /api/tasks/{id}` - Update task (200/404/422)
- `PATCH /api/tasks/{id}/complete` - Toggle completion (200/404)
- `DELETE /api/tasks/{id}` - Delete task (204/404)

## Documentation

- Swagger docs: http://localhost:8000/docs
- Specification: `/specs/003-fastapi-backend/spec.md`
- Implementation plan: `/specs/003-fastapi-backend/plan.md`
