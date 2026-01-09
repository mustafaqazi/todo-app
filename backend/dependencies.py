"""Dependency injection functions for FastAPI endpoints"""

import logging
from typing import Dict, Any

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from config import settings

logger = logging.getLogger(__name__)
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> Dict[str, Any]:
    """
    Extract and verify JWT token from Authorization header.

    This dependency:
    1. Extracts the JWT from the Authorization header (Bearer token)
    2. Verifies the signature using BETTER_AUTH_SECRET
    3. Extracts the user_id from the 'user_id' claim (custom Better Auth claim)
    4. Returns a dict with the user_id

    Args:
        credentials: HTTPAuthCredentials from the Authorization header

    Returns:
        Dict containing user_id extracted from JWT 'user_id' claim

    Raises:
        HTTPException: 401 Unauthorized if token is invalid, expired, or missing

    Example:
        ```python
        @app.get("/tasks")
        async def list_tasks(current_user: Dict = Depends(get_current_user)):
            user_id = current_user["user_id"]
            # Use user_id to filter tasks
        ```
    """
    token = credentials.credentials

    try:
        # Decode JWT with the shared secret
        payload = jwt.decode(
            token,
            settings.BETTER_AUTH_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
        )
    except jwt.ExpiredSignatureError:
        logger.warning(f"Expired JWT token attempted")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError as e:
        logger.warning(f"Invalid JWT token: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        logger.error(f"Unexpected error during JWT verification: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Extract user_id from 'user_id' claim (custom Better Auth claim, not standard 'sub')
    user_id = payload.get("user_id")
    if not user_id:
        logger.warning("JWT missing 'user_id' claim")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token format",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {"user_id": user_id}
