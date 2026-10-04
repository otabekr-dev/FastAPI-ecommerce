from pydantic import BaseModel, ConfigDict, computed_field
from app.products.schemas import ProductOut
from decimal import Decimal
from app.orders.models import Status
from datetime import datetime

class OrderItemOut(BaseModel):
    id: int
    product_id: int
    quantity: int
    price: Decimal
    product: ProductOut

    model_config = ConfigDict(from_attributes=True)

    @computed_field
    @property
    def subtotal(self) -> Decimal:
        return self.price * self.quantity
    
class OrderOut(BaseModel):
    id:int
    status:Status
    total_price: Decimal
    created_at: datetime
    items: list[OrderItemOut]

    model_config = ConfigDict(from_attributes=True)

class OrderStatusUpdate(BaseModel):
    status: Status    