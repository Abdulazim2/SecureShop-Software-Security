
import hashlib
import secrets

from fastapi import Request, Response
from sqlalchemy.orm import Session

from app.crud.cart import get_or_create_cart


COOKIE_NAME = "secureshop_cart_session"
COOKIE_MAX_AGE = 60 * 60 * 24 * 7


def hash_session_token(token: str) -> str:
    return hashlib.sha256(
        token.encode("utf-8")
    ).hexdigest()


def create_session_token() -> str:
    return secrets.token_urlsafe(32)


def get_cart_session(
    db: Session,
    request: Request,
    response: Response
):
    token = request.cookies.get(COOKIE_NAME)

    if not token:
        token = create_session_token()

        response.set_cookie(
            key=COOKIE_NAME,
            value=token,
            max_age=COOKIE_MAX_AGE,
            httponly=True,
            secure=False,
            samesite="lax",
            path="/"
        )

    token_hash = hash_session_token(token)

    cart = get_or_create_cart(db, token_hash)

    return cart
