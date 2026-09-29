from fastapi import HTTPException,  status
from sqlalchemy.orm import Session

from app.users import repository
from app.users.schemas import UserCreate
from app.users.models import User
from app.core.security import hash_password, verify_password

async def authenticate_user(db:Session, username:str, password:str) -> User:
    user = await repository.get_by_username(db, username)

    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect password or username'
        )

    return user

async def register_user(db: Session, user_data:UserCreate) -> User:
    existing_user = await repository.get_by_username(db, user_data.username)

    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Username already exists')

    hashed_password = hash_password(user_data.password)
    user = repository.create_user(db, user_data, hashed_password)

    return await user