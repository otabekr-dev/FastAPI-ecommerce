from pydantic import BaseModel, ConfigDict, Field, computed_field
from decimal import Decimal
from app.products.schemas import ProductOut



class CartItemAdd(BaseModel):
    product_id: int
    quantity: int = Field(default=1, gt=0, le=100)


class CartItemUpdate(BaseModel):
    quantity: int = Field(gt=0, le=100)


class CartItemOut(BaseModel):
    id: int
    quantity: int
    product: ProductOut

    model_config = ConfigDict(from_attributes=True)

    @computed_field
    @property
    def subtotal(self) -> Decimal:
        return self.product.price * self.quantity


class CartOut(BaseModel):
    id: int
    items: list[CartItemOut]

    model_config = ConfigDict(from_attributes=True)

    @computed_field
    @property
    def total(self) -> Decimal:
        return sum((item.subtotal for item in self.items), Decimal("0"))