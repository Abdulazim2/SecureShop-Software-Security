
import hashlib
import secrets

from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.email_verification import EmailVerificationToken


TOKEN_EXPIRE_MINUTES = 30


def hash_verification_token(token: str) -> str:
    return hashlib.sha256(
        token.encode("utf-8")
    ).hexdigest()


def create_verification_token(db: Session, user: User):
    # Invalidate previous unused tokens
    old_tokens = db.scalars(
        select(EmailVerificationToken).where(
            EmailVerificationToken.user_id == user.id,
            EmailVerificationToken.used_at.is_(None)
        )
    ).all()

    for old_token in old_tokens:
        old_token.used_at = datetime.now(timezone.utc)

    # Generate a cryptographically secure token
    raw_token = secrets.token_urlsafe(32)

    token_record = EmailVerificationToken(
        user_id=user.id,
        token_hash=hash_verification_token(raw_token),
        expires_at=datetime.now(timezone.utc) + timedelta(
            minutes=TOKEN_EXPIRE_MINUTES
        )
    )

    db.add(token_record)
    db.commit()

    return raw_token


def verify_email_token(db: Session, raw_token: str):
    token_hash = hash_verification_token(raw_token)

    token_record = db.scalar(
        select(EmailVerificationToken).where(
            EmailVerificationToken.token_hash == token_hash
        )
    )

    if token_record is None:
        return None

    if token_record.used_at is not None:
        return None

    now = datetime.now(timezone.utc)

    expires_at = token_record.expires_at

    # SQLite may return a naive datetime
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)

    if expires_at <= now:
        return None

    user = db.get(User, token_record.user_id)

    if user is None or not user.is_active:
        return None

    user.is_verified = True
    token_record.used_at = now

    db.commit()
    db.refresh(user)

    return user
