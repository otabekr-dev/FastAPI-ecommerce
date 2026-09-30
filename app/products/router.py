from fastapi import Depends, APIRouter, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.users.dependencies import require_admin, get_current_user
from app.products import service
from app.products.schemas import CategoryCreate, CategoryOut, ProductUpdate, ProductCreate, ProductOut
from app.products.models import Category, Product

router_product = APIRouter(prefix='/products', tags=['products'])
router_category = APIRouter(prefix='/category', tags=['category'])

@router_category.post('/create/', response_model=CategoryOut, dependencies=[Depends(require_admin)], status_code=201)
async def create_category(category_data: CategoryCreate, db: AsyncSession = Depends(get_db))-> Category:
    return await service.create_category(db, category_data) 

@router_category.get('/list/', response_model=list[CategoryOut], status_code=200)
async def list_category(db: AsyncSession = Depends(get_db)):
    return await service.list_categories(db)

@router_product.post('/create/', response_model=ProductOut, dependencies=[Depends(require_admin)], status_code=201)
async def create_product(product_data:ProductCreate, db:AsyncSession = Depends(get_db)):
    return await service.create_product(db, product_data)

@router_product.get('/list/', response_model=list[ProductOut], status_code=200)
async def list_products(
    category_id: int | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    return await service.list_products(db, skip, limit, category_id)

@router_product.patch('/patch/{product_id}/', response_model=ProductOut, dependencies=[Depends(require_admin)], status_code=200)
async def update_product(update_data: ProductUpdate, product_id: int ,db: AsyncSession = Depends(get_db)):
    return await service.update_product(db, update_data, product_id)

@router_product.get('/retrieve/{product_id}/', response_model=ProductOut,status_code=200)
async def retrieve_product(product_id:int, db:AsyncSession = Depends(get_db)):
    return await service.get_product(db, product_id)
