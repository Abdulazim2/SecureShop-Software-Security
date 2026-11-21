
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.product import ProductResponse, CategoryResponse
from app.crud.product import (
    get_products,
    get_product,
    get_categories,
    search_products,
    filter_products
)

router = APIRouter(
    prefix="/api",
    tags=["Products & Categories"]
)


# =========================
# Categories
# =========================

@router.get("/categories/", response_model=list[CategoryResponse])
def list_categories(
    db: Session = Depends(get_db)
):
    return get_categories(db)


# =========================
# List Products
# =========================

@router.get("/products/", response_model=list[ProductResponse])
def list_products(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    return get_products(
        db,
        skip=skip,
        limit=limit
    )


# =========================
# Search Products
# =========================

@router.get("/products/search/", response_model=list[ProductResponse])
def search_products_endpoint(
    keyword: str = Query(min_length=1, max_length=100),
    db: Session = Depends(get_db)
):
    return search_products(db, keyword)


# =========================
# Filter Products
# =========================

@router.get("/products/filter/", response_model=list[ProductResponse])
def filter_products_endpoint(
    category_id: int | None = Query(default=None, ge=1),
    min_price: float | None = Query(default=None, ge=0),
    max_price: float | None = Query(default=None, ge=0),
    in_stock: bool = Query(default=False),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    if (
        min_price is not None
        and max_price is not None
        and min_price > max_price
    ):
        raise HTTPException(
            status_code=422,
            detail="Minimum price cannot exceed maximum price"
        )

    return filter_products(
        db,
        category_id=category_id,
        min_price=min_price,
        max_price=max_price,
        in_stock=in_stock,
        skip=skip,
        limit=limit
    )


# =========================
# Product Details
# =========================

@router.get("/products/{product_id}", response_model=ProductResponse)
def product_details(
    product_id: int,
    db: Session = Depends(get_db)
):
    product = get_product(db, product_id)

    if product is None or not product.is_active:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product
