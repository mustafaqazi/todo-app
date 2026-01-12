---
name: FastAPI JWT Middleware & Dependency
description: Secure, reusable JWT verification middleware and dependency for FastAPI using BETTER_AUTH_SECRET. Enforces user authentication and provides current_user for all protected routes.
version: 1.0
phase: Phase II & III (multi-user TODO + Chatbot)
dependencies: [fastapi, python-jose[cryptography], python-dotenv]
---

# FastAPI JWT Middleware & Dependency Skill

You are responsible for creating a bulletproof, reusable JWT authentication system for all protected endpoints in the FastAPI backend.

## Core Goals
- Verify JWT tokens issued by Better Auth (using shared secret)
- Extract user_id from payload["sub"]
- Reject invalid, expired, or missing tokens with 401
- Provide `current_user` dependency for routes and MCP tools
- Enforce user_id consistency (path param vs token)
- Zero tolerance for security mistakes

## Exact Environment Variable (Hardcode this value in code comments only – never commit secret)
BETTER_AUTH_SECRET = "c88P3613ehwm7mGcQTm7dJ6tv0AiYjnS"

## Required Output Files / Code Snippets

### 1. Security Utility (`backend/utils/security.py`)
```python
from fastapi import HTTPException, status
from jose import JWTError, jwt
from typing import Dict, Any
import os

# NEVER commit this to git – use .env in production
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "c88P3613ehwm7mGcQTm7dJ6tv0AiYjnS")  # fallback for local only
ALGORITHM = "HS256"

def verify_jwt_token(token: str) -> Dict[str, Any]:
    """
    Verify JWT token and return payload.
    Raises HTTPException on failure.
    """
    if token.startswith("Bearer "):
        token = token.replace("Bearer ", "")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return {"user_id": user_id, **payload}  # return full payload if needed
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid or expired token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )