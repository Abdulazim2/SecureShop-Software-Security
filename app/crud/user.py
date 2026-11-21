
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserRegister
from app.core.security import hash_password


def get_user_by_email(db: Session, email: str):
    normalized_email = email.strip().lower()

    return db.scalar(
        select(User).where(
            User.email == normalized_email
        )
    )


def get_user_by_id(db: Session, user_id: int):
    return db.get(User, user_id)


def create_user(db: Session, user_data: UserRegister):
    normalized_email = user_data.email.strip().lower()

    existing_user = get_user_by_email(
        db,
        normalized_email
    )

    if existing_user:
        raise ValueError("Email already registered")

    user = User(
        email=normalized_email,
        full_name=user_data.full_name.strip(),
        password_hash=hash_password(user_data.password),
        role="customer",
        is_active=True,
        is_verified=False
    )

    db.add(user)

    try:
        db.commit()
        db.refresh(user)
    except Exception:
        db.rollback()
        raise

    return user
