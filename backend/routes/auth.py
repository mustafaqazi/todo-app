"""Authentication endpoints: signup, login, and token verification."""

from fastapi import APIRouter, Depends, HTTPException, Header, status
from sqlmodel import Session, select
from typing import Optional

from db import get_session
from dependencies import get_current_user
from src.models import User
from schemas import UserSignup, UserLogin, AuthResponse, VerifyResponse
from utils.password import hash_password, verify_password, validate_password_strength
from utils.jwt import create_access_token, decode_token
from config import settings

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/api/auth/sign-up/email", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def signup(
    user_data: UserSignup,
    session: Session = Depends(get_session),
) -> AuthResponse:
    """
    Register a new user with email and password.

    Args:
        user_data: UserSignup schema with email and password
        session: Database session (injected)

    Returns:
        AuthResponse with access_token and user_id

    Raises:
        HTTPException: 400 if email exists, 422 if password invalid
    """
    # Validate password strength
    is_valid, message = validate_password_strength(user_data.password)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Password validation failed: {message}"
        )

    # Check if user already exists
    result = await session.execute(
        select(User).where(User.email == user_data.email)
    )
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    # Create new user with hashed password
    hashed_pwd = hash_password(user_data.password)
    new_user = User(
        email=user_data.email,
        hashed_password=hashed_pwd,
    )

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    # Generate JWT token with user_id as subject (sub claim)
    user_id = str(new_user.id)
    access_token = create_access_token(
        user_id=user_id,
        secret=settings.BETTER_AUTH_SECRET,
    )

    return AuthResponse(
        access_token=access_token,
        token_type="bearer",
        user_id=user_id,
    )


@router.post("/api/auth/login/email", response_model=AuthResponse)
async def login(
    user_data: UserLogin,
    session: Session = Depends(get_session),
) -> AuthResponse:
    """
    Authenticate user with email and password.

    Args:
        user_data: UserLogin schema with email and password
        session: Database session (injected)

    Returns:
        AuthResponse with access_token and user_id

    Raises:
        HTTPException: 401 if credentials invalid
    """
    # Find user by email
    result = await session.execute(
        select(User).where(User.email == user_data.email)
    )
    user = result.scalar_one_or_none()

    # Verify password (returns False for non-existent user)
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Generate JWT token with 'sub' claim
    user_id = str(user.id)
    access_token = create_access_token(
        user_id=user_id,
        secret=settings.BETTER_AUTH_SECRET,
    )

    return AuthResponse(
        access_token=access_token,
        token_type="bearer",
        user_id=user_id,
    )


@router.get("/verify", response_model=VerifyResponse)
async def verify_token(
    authorization: Optional[str] = Header(None),
) -> VerifyResponse:
    """
    Verify a JWT token without requiring database access.

    Args:
        authorization: Authorization header with Bearer token

    Returns:
        VerifyResponse with validity status and user_id if valid
    """
    if not authorization or not authorization.startswith("Bearer "):
        return VerifyResponse(valid=False, user_id=None)

    token = authorization.split(" ", 1)[1]

    try:
        payload = decode_token(
            token=token,
            secret=settings.BETTER_AUTH_SECRET,
        )
        user_id = payload.get("sub")

        if not user_id:
            return VerifyResponse(valid=False, user_id=None)

        return VerifyResponse(valid=True, user_id=user_id)

    except Exception:
        # Token is invalid, expired, or malformed
        return VerifyResponse(valid=False, user_id=None)
