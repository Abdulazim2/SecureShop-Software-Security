
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.product import Product, Category
from app.schemas.product import ProductCreate, ProductUpdate, CategoryCreate


# =========================
# Category CRUD
# =========================

def get_category(db: Session, category_id: int):
    return db.get(Category, category_id)


def get_categories(db: Session):
    return db.scalars(
        select(Category).order_by(Category.name)
    ).all()


def create_category(db: Session, category_data: CategoryCreate):
    category = Category(**category_data.model_dump())

    db.add(category)

    try:
        db.commit()
        db.refresh(category)
    except Exception:
        db.rollback()
        raise

    return category


# =========================
# Product CRUD
# =========================

def get_product(db: Session, product_id: int):
    return db.get(Product, product_id)


def get_products(
    db: Session,
    skip: int = 0,
    limit: int = 20
):
    limit = min(max(limit, 1), 100)
    skip = max(skip, 0)

    statement = (
        select(Product)
        .where(Product.is_active.is_(True))
        .order_by(Product.id)
        .offset(skip)
        .limit(limit)
    )

    return db.scalars(statement).all()


# =========================
# Secure Product Search
# =========================

def search_products(db: Session, keyword: str):
    keyword = keyword.strip()

    if not keyword or len(keyword) > 100:
        return []

    statement = (
        select(Product)
        .where(
            Product.is_active.is_(True),
            Product.name.ilike(f"%{keyword}%")
        )
        .order_by(Product.name)
        .limit(100)
    )

    return db.scalars(statement).all()


# =========================
# Product Filtering
# =========================

def filter_products(
    db: Session,
    category_id: int | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    in_stock: bool = False,
    skip: int = 0,
    limit: int = 20
):
    limit = min(max(limit, 1), 100)
    skip = max(skip, 0)

    statement = select(Product).where(
        Product.is_active.is_(True)
    )

    if category_id is not None:
        statement = statement.where(
            Product.category_id == category_id
        )

    if min_price is not None:
        statement = statement.where(
            Product.price >= min_price
        )

    if max_price is not None:
        statement = statement.where(
            Product.price <= max_price
        )

    if in_stock:
        statement = statement.where(
            Product.stock > 0
        )

    statement = (
        statement
        .order_by(Product.id)
        .offset(skip)
        .limit(limit)
    )

    return db.scalars(statement).all()


# =========================
# Create Product
# =========================

def create_product(db: Session, product_data: ProductCreate):
    data = product_data.model_dump()

    category_id = data.get("category_id")

    if category_id is not None and db.get(Category, category_id) is None:
        raise ValueError("Category not found")

    product = Product(**data)

    db.add(product)

    try:
        db.commit()
        db.refresh(product)
    except Exception:
        db.rollback()
        raise

    return product


# =========================
# Update Product
# =========================

def update_product(
    db: Session,
    product_id: int,
    product_data: ProductUpdate
):
    product = db.get(Product, product_id)

    if product is None:
        return None

    data = product_data.model_dump(exclude_unset=True)

    if "category_id" in data and data["category_id"] is not None:
        if db.get(Category, data["category_id"]) is None:
            raise ValueError("Category not found")

    for field, value in data.items():
        setattr(product, field, value)

    try:
        db.commit()
        db.refresh(product)
    except Exception:
        db.rollback()
        raise

    return product


# =========================
# Deactivate Product
# =========================

def deactivate_product(db: Session, product_id: int):
    product = db.get(Product, product_id)

    if product is None:
        return None

    product.is_active = False

    try:
        db.commit()
        db.refresh(product)
    except Exception:
        db.rollback()
        raise

    return product
