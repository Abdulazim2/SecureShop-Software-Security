
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.cart import (
    CartItemAdd,
    CartItemUpdate,
    CartResponse
)
from app.services.cart_session import get_cart_session
from app.crud.cart import (
    add_item_to_cart,
    update_cart_item,
    remove_cart_item,
    clear_cart,
    calculate_cart_response
)


router = APIRouter(
    prefix="/api/cart",
    tags=["Shopping Cart"]
)


def get_current_cart(
    request: Request,
    response: Response,
    db: Session = Depends(get_db)
):
    return get_cart_session(db, request, response)


@router.get("/", response_model=CartResponse)
def view_cart(
    cart=Depends(get_current_cart)
):
    return calculate_cart_response(cart)


@router.post("/items/", response_model=CartResponse)
def add_cart_item(
    item_data: CartItemAdd,
    cart=Depends(get_current_cart),
    db: Session = Depends(get_db)
):
    try:
        updated_cart = add_item_to_cart(
            db,
            cart,
            item_data.product_id,
            item_data.quantity
        )

        return calculate_cart_response(updated_cart)

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


@router.put("/items/{item_id}", response_model=CartResponse)
def update_cart_item_endpoint(
    item_id: int,
    item_data: CartItemUpdate,
    cart=Depends(get_current_cart),
    db: Session = Depends(get_db)
):
    try:
        updated_cart = update_cart_item(
            db,
            cart,
            item_id,
            item_data.quantity
        )

        if updated_cart is None:
            raise HTTPException(
                status_code=404,
                detail="Cart item not found"
            )

        return calculate_cart_response(updated_cart)

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


@router.delete("/items/{item_id}", response_model=CartResponse)
def delete_cart_item(
    item_id: int,
    cart=Depends(get_current_cart),
    db: Session = Depends(get_db)
):
    updated_cart = remove_cart_item(
        db,
        cart,
        item_id
    )

    if updated_cart is None:
        raise HTTPException(
            status_code=404,
            detail="Cart item not found"
        )

    return calculate_cart_response(updated_cart)


@router.delete("/", response_model=CartResponse)
def empty_cart(
    cart=Depends(get_current_cart),
    db: Session = Depends(get_db)
):
    updated_cart = clear_cart(db, cart)

    return calculate_cart_response(updated_cart)
