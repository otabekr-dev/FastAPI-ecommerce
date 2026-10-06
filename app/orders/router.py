from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.users.dependencies import require_admin, get_current_user
from app.users.models import User
from app.orders import service
from app.orders.schemas import OrderOut, OrderStatusUpdate


router = APIRouter(prefix='/orders', tags=['orders'])

@router.post(path='/create/', response_model=OrderOut, status_code=201)
async def create_order(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await service.checkout(db, user_id=user.id)

@router.get(path='/list/', response_model=list[OrderOut], status_code=200)
async def list_my_orders(
    user:User = Depends(get_current_user),
    skip: int = Query(ge=0, default=0),
    limit: int = Query(gt=0, le=100 ,default=20),
    db: AsyncSession = Depends(get_db)
):
    return await service.list_my_orders(db, user_id=user.id, skip=skip, limit=limit)

@router.get(path='/get/{order_id}/', response_model=OrderOut, status_code=200)
async def get_my_order(
    order_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):   
    return await service.get_my_order(db, user_id=user.id, order_id=order_id)

@router.patch(path='/update/{order_id}/', response_model=OrderOut, status_code=200, dependencies=[Depends(require_admin)])
async def update_status(order_id:int, data:OrderStatusUpdate, db:AsyncSession=Depends(get_db)):
    return await service.change_status(db, order_id=order_id, new_status=data.status)

