
from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.database import Base, engine
from app.models import Product, Category, Cart, CartItem, User
from app.routers.products import router as products_router
from app.routers.cart import router as cart_router
from app.routers.auth import router as auth_router
from app.core.rate_limit import limiter

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SecureShop API",
    description="Secure E-Commerce Platform",
    version="1.0.0"
)

# Rate Limiting Configuration
app.state.limiter = limiter
app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler
)

app.include_router(products_router)
app.include_router(cart_router)
app.include_router(auth_router)


@app.get("/")
def home():
    return {
        "message": "Welcome to SecureShop",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "database": "connected"
    }
