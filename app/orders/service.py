from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from decimal import Decimal

from app.orders import repository
from app.orders.models import Order, Status
from app.products import repository as product_repository
from app.cart import repository as cart_repository

ALLOWED_TRANSITIONS = {
    Status.PENDING: [Status.PAID, Status.CANCELLED],
    Status.PAID: [Status.SHIPPED, Status.CANCELLED],
    Status.SHIPPED: [Status.DELIVERED],
    Status.DELIVERED: [],
    Status.CANCELLED: [],
}

async def checkout(db:AsyncSession, user_id:int) -> Order:
    cart = await cart_repository.get_cart_by_user_id(db, user_id=user_id)

    if cart is None or not cart.items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Empty cart'
        )

    product_ids = []
    for i in cart.items:
        product_ids.append(i.product_id) 

    await product_repository.get_products_for_update(db, product_ids=product_ids)

    order_items = []
    total_price = Decimal(0)

    for item in cart.items:
        product = item.product
        
        if not product.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Product {product.name} is not available'
            )

        if item.quantity > product.stock:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Not enough stock'
            )

        order_items.append({
            'product_id': product.id,
            'quantity':item.quantity,
            'price':product.price
        })

        total_price += product.price * item.quantity

    order = await repository.create_order(db, user_id=user_id, total_price=total_price, items=order_items)

    for item in cart.items:
        item.product.stock -= item.quantity        

    await cart_repository.clear_cart(db, cart_id=cart.id)

    await db.commit()
    await db.refresh(order)

    return order

async def list_my_orders(
    db: AsyncSession, user_id: int, skip: int = 0, limit: int = 20
) -> list[Order]:
    return await repository.get_order_by_user(
        db, user_id=user_id, skip=skip, limit=limit
    )


async def get_my_order(db: AsyncSession, user_id: int, order_id: int) -> Order:
    order = await repository.get_order_by_id(db, order_id=order_id)

    if order is None or order.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Order not found'
        )

    return order


async def change_status(db: AsyncSession, order_id: int, new_status: Status) -> Order:
    order = await repository.get_order_by_id(db, order_id=order_id)

    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Order not found'
        )

    if new_status not in ALLOWED_TRANSITIONS[order.status]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Cannot change status from {order.status.value} to {new_status.value}'
        )

    if new_status == Status.CANCELLED and order.status != Status.CANCELLED:
        product_ids = []

        for item in order.items:
            product_ids.append(item.product_id)

        await product_repository.get_products_for_update(db, product_ids=product_ids)

        for item in order.items:
            item.product.stock += item.quantity

    return await repository.update_status(db, order=order, new_status=new_status)