"""JWT token generation and verification utilities."""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import jwt

# Note: The JWT_SECRET should be loaded from environment in the calling code
# This module provides pure functions for token generation


def create_access_token(
    user_id: str,
    secret: str,
    expires_in_hours: int = 24,
    algorithm: str = "HS256"
) -> str:
    """
    Create a JWT access token.

    Args:
        user_id: User identifier (will be stored in 'sub' claim)
        secret: Secret key for signing (BETTER_AUTH_SECRET)
        expires_in_hours: Token expiration time in hours (default 24)
        algorithm: JWT algorithm (default HS256)

    Returns:
        Encoded JWT token string

    Raises:
        ValueError: If secret is empty or user_id is empty
    """
    if not secret or not user_id:
        raise ValueError("Secret and user_id are required")

    now = datetime.utcnow()
    expires = now + timedelta(hours=expires_in_hours)

    payload: Dict[str, Any] = {
        "sub": user_id,  # Standard JWT claim for subject (user identifier)
        "iat": now,      # Issued at
        "exp": expires,  # Expiration time
    }

    token = jwt.encode(payload, secret, algorithm=algorithm)
    return token


def decode_token(
    token: str,
    secret: str,
    algorithm: str = "HS256",
    options: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Decode and verify a JWT token.

    Args:
        token: JWT token string to decode
        secret: Secret key for verification (BETTER_AUTH_SECRET)
        algorithm: JWT algorithm (default HS256)
        options: Additional jose decode options

    Returns:
        Decoded token payload as dict

    Raises:
        JWTError: If token is invalid, expired, or signature doesn't match
    """
    decode_options = {"verify_aud": False}
    if options:
        decode_options.update(options)

    payload = jwt.decode(
        token,
        secret,
        algorithms=[algorithm],
        options=decode_options
    )

    return payload


def get_user_id_from_token(
    token: str,
    secret: str,
    algorithm: str = "HS256"
) -> Optional[str]:
    """
    Extract user_id from a JWT token's 'sub' claim.

    Args:
        token: JWT token string
        secret: Secret key for verification
        algorithm: JWT algorithm (default HS256)

    Returns:
        User ID (sub claim) if token is valid, None otherwise

    Note:
        This function catches exceptions silently and returns None for invalid tokens.
    """
    try:
        payload = decode_token(token, secret, algorithm)
        return payload.get("sub")
    except Exception:
        return None
