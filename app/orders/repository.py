from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.orders.models import OrderItem, Order, Status
from decimal import Decimal
from sqlalchemy.orm import selectinload
    

async def create_order(db:AsyncSession, user_id:int, total_price:Decimal, items:list[dict]) -> Order:
    order = Order(
        user_id=user_id,
        total_price=total_price,
        items=[OrderItem(**item) for item in items]
    )

    db.add(order)
    await db.flush()

    return order

async def get_order_by_id(db: AsyncSession, order_id:int) -> Order | None:
    result = await db.execute(select(Order).where(Order.id==order_id).options(selectinload(Order.items).selectinload(OrderItem.product)))
    
    return result.scalar_one_or_none()

async def get_order_by_user(db: AsyncSession, user_id:int, skip:int = 0, limit:int = 20) -> list[Order]:
    result = await db.execute(select(Order).where(Order.user_id==user_id).order_by(Order.created_at.desc()).offset(skip).limit(limit))

    return list(result.scalars().all())

async def update_status(db:AsyncSession, order:Order, new_status:Status)-> Order:
    order.status = new_status

    await db.commit()

    return get_order_by_id(db, order_id=order.id)