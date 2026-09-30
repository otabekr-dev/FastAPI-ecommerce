from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.products.models import Product, Category
from app.products.schemas import CategoryCreate

async def get_category_by_id(db: AsyncSession, category_id:int) -> Category | None:
    result = await db.execute(select(Category).where(Category.id==category_id))
    return result.scalar_one_or_none()

async def get_category_by_name(db: AsyncSession, category_name:str) -> Category | None:
    result = await db.execute(select(Category).where(Category.name==category_name))
    return result.scalar_one_or_none()

async def get_categories(db:AsyncSession) -> list[Category]:
    result = await db.execute(select(Category).order_by(Category.id))
    return list(result.scalars().all())

async def create_category(db:AsyncSession, category_data:dict) -> Category:
    category = Category(**category_data)

    db.add(category)
    await db.commit()
    await db.refresh(category)

    return category

async def get_product_by_id(db: AsyncSession, product_id: int) -> Product | None:
    result = await db.execute(select(Product).where(Product.id==product_id))
    return result.scalar_one_or_none()


async def create_product(db: AsyncSession, product_data: dict) -> Product:
    product = Product(**product_data)

    db.add(product)
    await db.commit()
    await db.refresh(product)

    return product

async def get_products(
    db:AsyncSession,
    skip: int = 0,
    limit:int = 20,
    category_id:int | None = None
) -> list[Product]:
    query = select(Product).where(Product.is_active.is_(True))

    if category_id is not None:
        query = query.where(Product.category_id==category_id)

    query = query.order_by(Product.id).offset(skip).limit(limit)

    result = await db.execute(query)

    return list(result.scalars().all()) 
    

async def update_product(db: AsyncSession, product: Product, update_data: dict) -> Product:
    for field , value in update_data.items():
        setattr(product, field, value)

    await db.commit()
    await db.refresh(product)

    return product
