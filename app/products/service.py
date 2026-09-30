from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.products import repository
from app.products.schemas import ProductCreate, CategoryCreate, ProductUpdate
from app.products.models import Category, Product


async def create_category(db: AsyncSession, category_data: CategoryCreate) -> Product:
    existing_category = await repository.get_category_by_name(db, category_data.name)

    if existing_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Category already exists'
        )

    category = await repository.create_category(db, category_data.model_dump())

    return category


async def list_categories(db:AsyncSession) -> list[Category]:
    return await repository.get_categories(db)


async def create_product(db: AsyncSession, product_data: ProductCreate) -> Product:
    category = await repository.get_category_by_id(db, product_data.category_id)

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Category not found'
        )

    product = await repository.create_product(db, product_data.model_dump())

    return product

async def get_product(db:AsyncSession, product_id:int) -> Product:
    product = await repository.get_product_by_id(db, product_id)

    if product is None or not product.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Product not found'
        )

    return product

async def update_product(db: AsyncSession, update_data: ProductUpdate, product_id: int) -> Product:
    product = await repository.get_product_by_id(db, product_id)

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found')

    data = update_data.model_dump(exclude_unset=True, exclude_none=True)

    new_category_id = data.get('category_id')

    if new_category_id is not None:
        category = await repository.get_category_by_id(db, new_category_id)

        if category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Category not found'
            )

    return await repository.update_product(db, product, data)        

async def list_products(
    db: AsyncSession,
    skip: int,
    limit: int,
    category_id: int | None = None
) -> list[Product]:
    return await repository.get_products(db, skip=skip, limit=limit, category_id=category_id)