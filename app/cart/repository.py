from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.cart.models import CartItems, Cart

async def get_cart_by_user_id(db:AsyncSession, user_id:int) -> Cart | None:
    result = await db.execute(select(Cart).where(Cart.user_id==user_id))
    return result.scalar_one_or_none()

async def create_cart(db:AsyncSession, user_id:int) -> Cart:
    cart = Cart(
        user_id=user_id
    )

    db.add(cart)
    await db.commit()
    await db.refresh(cart)

    return cart

async def get_item_by_product(db:AsyncSession, cart_id:int, product_id:int) -> CartItems | None:
    result = await db.execute(select(CartItems).where(CartItems.product_id==product_id, CartItems.cart_id==cart_id))
    return result.scalar_one_or_none()

async def get_item_by_id(db:AsyncSession, item_id:int, cart_id:int) -> CartItems | None:
    result = await db.execute(select(CartItems).where(CartItems.id==item_id, CartItems.cart_id==cart_id))
    return result.scalar_one_or_none()

async def add_item(db:AsyncSession, cart_id:int, product_id:int, quantity:int) -> CartItems:
    cart_item = CartItems(
        cart_id=cart_id,
        product_id=product_id,
        quantity=quantity
    )

    db.add(cart_item)
    await db.commit()
    await db.refresh(cart_item)

    return cart_item

async def update_item_quantity(db:AsyncSession, item:CartItems, quantity:int) -> CartItems:
    item.quantity = quantity

    await db.commit()
    await db.refresh(item)

    return item

async def delete_item(db:AsyncSession, item:CartItems):
    await db.delete(item)
    await db.commit()

async def clear_cart(db:AsyncSession, cart_id:int) -> None:
    await db.execute(delete(CartItems).where(CartItems.cart_id==cart_id))
    