
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user import UserRegister
from app.crud.user import create_user, get_user_by_email
from app.core.security import verify_password, create_access_token
from app.core.rate_limit import limiter
from app.services.email_verification import (
    create_verification_token,
    verify_email_token
)
from app.dependencies import get_current_user
from app.models.user import User


router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)


@router.post("/register", status_code=status.HTTP_201_CREATED)
@limiter.limit("3/minute")
def register(
    request: Request,
    user_data: UserRegister,
    db: Session = Depends(get_db)
):
    try:
        user = create_user(db, user_data)

        verification_token = create_verification_token(db, user)

        # Development only: never expose this token in production.
        return {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role,
            "is_active": user.is_active,
            "is_verified": user.is_verified,
            "verification_token": verification_token
        }

    except ValueError as error:
        raise HTTPException(
            status_code=409,
            detail=str(error)
        )


@router.post("/verify-email")
def verify_email(
    token: str,
    db: Session = Depends(get_db)
):
    user = verify_email_token(db, token)

    if user is None:
        raise HTTPException(
            status_code=400,
            detail="Invalid, expired, or already used verification token"
        )

    return {
        "message": "Email verified successfully",
        "user_id": user.id
    }


@router.post("/login")
@limiter.limit("5/minute")
def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    email = form_data.username.strip().lower()

    user = get_user_by_email(db, email)

    if user is None or not verify_password(
        form_data.password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    if not user.is_active:
        raise HTTPException(
            status_code=403,
            detail="Account is disabled"
        )

    if not user.is_verified:
        raise HTTPException(
            status_code=403,
            detail="Email address is not verified"
        )

    access_token = create_access_token(
        user_id=user.id,
        role=user.role
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.get("/me")
def get_my_profile(
    current_user: User = Depends(get_current_user)
):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "role": current_user.role,
        "is_active": current_user.is_active,
        "is_verified": current_user.is_verified
    }
