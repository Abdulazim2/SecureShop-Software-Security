
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models.cart import Cart, CartItem
from app.models.product import Product


MAX_CART_ITEM_QUANTITY = 1000


def get_cart_by_token_hash(db: Session, token_hash: str):
    statement = (
        select(Cart)
        .options(
            joinedload(Cart.items).joinedload(CartItem.product)
        )
        .where(Cart.session_token_hash == token_hash)
    )

    return db.scalars(statement).unique().first()


def get_or_create_cart(db: Session, token_hash: str):
    cart = db.scalar(
        select(Cart).where(
            Cart.session_token_hash == token_hash
        )
    )

    if cart is None:
        cart = Cart(session_token_hash=token_hash)
        db.add(cart)
        db.commit()
        db.refresh(cart)

    return cart


def get_cart_details(db: Session, cart_id: int):
    statement = (
        select(Cart)
        .options(
            joinedload(Cart.items).joinedload(CartItem.product)
        )
        .where(Cart.id == cart_id)
    )

    return db.scalars(statement).unique().first()


def validate_quantity(quantity: int):
    if not isinstance(quantity, int) or isinstance(quantity, bool):
        raise ValueError("Quantity must be an integer")

    if quantity < 1 or quantity > MAX_CART_ITEM_QUANTITY:
        raise ValueError(
            f"Quantity must be between 1 and {MAX_CART_ITEM_QUANTITY}"
        )


def add_item_to_cart(
    db: Session,
    cart: Cart,
    product_id: int,
    quantity: int
):
    validate_quantity(quantity)

    product = db.get(Product, product_id)

    if product is None or not product.is_active:
        raise ValueError("Product not found")

    item = db.scalar(
        select(CartItem).where(
            CartItem.cart_id == cart.id,
            CartItem.product_id == product_id
        )
    )

    current_quantity = item.quantity if item is not None else 0
    new_quantity = current_quantity + quantity

    if new_quantity > MAX_CART_ITEM_QUANTITY:
        raise ValueError("Maximum cart quantity exceeded")

    if new_quantity > product.stock:
        raise ValueError("Requested quantity exceeds available stock")

    if item is not None:
        item.quantity = new_quantity
    else:
        item = CartItem(
            cart_id=cart.id,
            product_id=product_id,
            quantity=quantity
        )
        db.add(item)

    try:
        db.commit()
    except Exception:
        db.rollback()
        raise

    return get_cart_details(db, cart.id)


def update_cart_item(
    db: Session,
    cart: Cart,
    item_id: int,
    quantity: int
):
    validate_quantity(quantity)

    item = db.scalar(
        select(CartItem)
        .join(Product)
        .where(
            CartItem.id == item_id,
            CartItem.cart_id == cart.id,
            Product.is_active.is_(True)
        )
    )

    if item is None:
        return None

    if quantity > item.product.stock:
        raise ValueError("Requested quantity exceeds available stock")

    item.quantity = quantity

    try:
        db.commit()
    except Exception:
        db.rollback()
        raise

    return get_cart_details(db, cart.id)


def remove_cart_item(
    db: Session,
    cart: Cart,
    item_id: int
):
    item = db.scalar(
        select(CartItem).where(
            CartItem.id == item_id,
            CartItem.cart_id == cart.id
        )
    )

    if item is None:
        return None

    db.delete(item)

    try:
        db.commit()
    except Exception:
        db.rollback()
        raise

    return get_cart_details(db, cart.id)


def clear_cart(db: Session, cart: Cart):
    try:
        db.query(CartItem).filter(
            CartItem.cart_id == cart.id
        ).delete(synchronize_session=False)

        db.commit()
    except Exception:
        db.rollback()
        raise

    return get_cart_details(db, cart.id)


def calculate_cart_response(cart: Cart):
    items = []
    total_quantity = 0
    total_price = Decimal("0.00")

    for item in cart.items:
        if item.product is None or not item.product.is_active:
            continue

        unit_price = Decimal(str(item.product.price))
        line_total = unit_price * item.quantity

        items.append({
            "id": item.id,
            "product_id": item.product_id,
            "product_name": item.product.name,
            "unit_price": unit_price,
            "quantity": item.quantity,
            "line_total": line_total
        })

        total_quantity += item.quantity
        total_price += line_total

    return {
        "id": cart.id,
        "items": items,
        "total_quantity": total_quantity,
        "total_price": total_price
    }
