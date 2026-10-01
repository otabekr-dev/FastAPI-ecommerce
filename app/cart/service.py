from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.cart import repository
from app.cart.schemas import CartItemAdd, CartItemUpdate
from app.cart.models import CartItems, Cart

async def create_cart(db:AsyncSession, user_id:int) -> Cart:
    existing_cart = await repository.get_cart_by_user_id(db, user_id=user_id)

    if existing_cart:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Cart already exists'
        )

    cart = repository.create_cart(db, user_id)

    return cart

async def get_cart_by_user_id(db:AsyncSession, user_id:int) -> Cart | None:
    cart = await repository.get_cart_by_user_id(db, user_id=user_id)

    return cart

async def get_cart_item_by_product(db:AsyncSession, cart_id:int, product_id:int) -> CartItems | None:
    cart_item = await repository.get_item_by_product(db, cart_id=cart_id, product_id=product_id)

    return cart_item

async def get_cart_item_by_id(db:AsyncSession, item_id:int, cart_id:int) -> CartItems | None:
    cart_item = await repository.get_item_by_id(db, item_id=item_id, cart_id=cart_id)

    return cart_item

async def add_item(db:AsyncSession, cart_id:int, product_id:int, quantity:int) -> CartItems:
    cart_item = await repository.add_item(db, cart_id=cart_id, product_id=product_id, quantity=quantity)

    return cart_item

async def update_item_quantity(db:AsyncSession, item:CartItems, quantity:CartItemUpdate) -> CartItems:
    item = await repository.get_item_by_id(db, item_id=item.id, cart_id=item.cart_id)

    if not item :
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Item not found'
        )

    updated_item = await repository.update_item_quantity(db, item=item, quantity=quantity)

    return updated_item

async def delete_item(db:AsyncSession, item:CartItems):
    item = await repository.get_item_by_id(db, item_id=item.id, cart_id=item.cart_id)

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Item not found'
        )

    deleted = await repository.delete_item(db, item=item)

    