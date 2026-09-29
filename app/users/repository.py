from sqlalchemy.ext.asyncio import AsyncSession
from app.users.models import User
from app.users.schemas import UserCreate
from sqlalchemy import select

async def get_by_username(db:AsyncSession, username:str)-> User | None:
    result = await db.execute(select(User).where(User.username==username))
    return result.scalar_one_or_none()

async def get_by_id(db:AsyncSession, user_id:int) -> User | None:
    result = await db.execute(select(User).where(User.id==user_id))
    return result.scalar_one_or_none()

async def create_user(db:AsyncSession, data:UserCreate, hashed_password:str) -> User:
    user = User(
        username=data.username,
        hashed_password=hashed_password
    )

    db.add(user)
    await db.commit()
    await db.refresh(user)

    return user