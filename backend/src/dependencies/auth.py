"""JWT authentication dependency."""

from fastapi import HTTPException, Header
from jose import jwt, JWTError
from typing import Dict, Optional

from ..config import settings


async def get_current_user(authorization: Optional[str] = Header(None)) -> Dict[str, str]:
    """
    Extract and verify JWT token from Authorization header.

    Returns:
        Dict with user_id extracted from JWT sub claim

    Raises:
        HTTPException: 401 if token missing, invalid, or malformed
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Missing or invalid authorization header"
        )

    token = authorization.split(" ", 1)[1]

    try:
        payload = jwt.decode(
            token,
            settings.BETTER_AUTH_SECRET,
            algorithms=["HS256"],
            options={"verify_aud": False}  # Don't validate audience claim
        )
        user_id = payload.get("sub")

        if not user_id:
            raise HTTPException(
                status_code=401,
                detail="Invalid token: missing user_id"
            )

        return {"user_id": user_id}

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )
