from fastapi import APIRouter,Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.users.dependencies import get_current_user
from app.users.models import User
from app.cart import service
from app.cart.schemas import CartItemUpdate, CartOut, CartItemAdd

router = APIRouter(prefix='/cart', tags=['cart'])


@router.get('/list/', response_model=CartOut, status_code=200)
async def get_or_create_cart(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
   return await service.get_or_create_cart(db, user_id=current_user.id)

@router.post('/items/', response_model=CartOut, status_code=201)
async def add_item(
    data: CartItemAdd,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
   return await service.add_item(db, cart_data=data, user_id=current_user.id)

@router.patch('/items/{item_id}/', response_model=CartOut, status_code=200)
async def update_item(
   data: CartItemUpdate,
   item_id:int,
   current_user: User = Depends(get_current_user),
   db: AsyncSession = Depends(get_db)
):
   return await service.update_item(db, user_id=current_user.id, item_id=item_id, data=data)

@router.delete('/items/{item_id}/', response_model=CartOut, status_code=200)
async def delete_item(
   item_id:int,
   current_user: User = Depends(get_current_user),
   db: AsyncSession = Depends(get_db)
):
   return await service.remove_item(db, user_id=current_user.id, item_id=item_id)
