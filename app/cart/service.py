from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.cart import repository
from app.products import repository as products_repository
from app.cart.schemas import CartItemAdd, CartItemUpdate
from app.cart.models import Cart

async def get_or_create_cart(db:AsyncSession, user_id:int) -> Cart:
    existing_cart = await repository.get_cart_by_user_id(db, user_id=user_id)

    if existing_cart:
        return existing_cart

    new_cart = Cart(
        user_id=user_id
    )

    db.add(new_cart)
    await db.commit()
    await db.refresh(new_cart)

    return new_cart

async def add_item(db:AsyncSession, cart_data:CartItemAdd, user_id:int) -> Cart:
    existing_cart = await get_or_create_cart(db, user_id)

    product = await products_repository.get_product_by_id(db, cart_data.product_id)

    if product is None or not product.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Product not found'
        )

    item = await repository.get_item_by_product(db, cart_id=existing_cart.id, product_id=product.id)
    
    new_quantity = cart_data.quantity + (item.quantity if item else 0)

    if new_quantity > product.stock:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Not enough stock'
        )

    if item:
        item = await repository.update_item_quantity(db, item=item, quantity=new_quantity)
    else:
        await repository.add_item(db, cart_id=existing_cart.id, product_id=product.id, quantity=new_quantity)

    await db.refresh(existing_cart, attribute_names=['items'])

    return existing_cart
    
async def update_item(db:AsyncSession, user_id:int, item_id:int, data:CartItemUpdate) -> Cart:
    cart = await get_or_create_cart(db, user_id=user_id)

    item = await repository.get_item_by_id(db, item_id=item_id, cart_id=cart.id)

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Item not found'
        )


    if data.quantity > item.product.stock:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Not enough stock'
        )

    await repository.update_item_quantity(db, item=item, quantity=data.quantity)
    await db.refresh(cart, attribute_names=['items'])

    return cart

async def remove_item(db:AsyncSession, user_id:int, item_id:int) -> Cart:
    cart = await get_or_create_cart(db, user_id=user_id)

    item = await repository.get_item_by_id(db, item_id=item_id, cart_id=cart.id)

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Item not found'
        )

    await repository.delete_item(db, item=item)
    await db.refresh(cart, attribute_names=['items'])

    return cart