
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class CartItemAdd(BaseModel):
    product_id: int = Field(ge=1)
    quantity: int = Field(default=1, ge=1, le=1000)


class CartItemUpdate(BaseModel):
    quantity: int = Field(ge=1, le=1000)


class CartItemResponse(BaseModel):
    id: int
    product_id: int
    product_name: str
    unit_price: Decimal
    quantity: int
    line_total: Decimal


class CartResponse(BaseModel):
    id: int
    items: list[CartItemResponse]
    total_quantity: int
    total_price: Decimal
