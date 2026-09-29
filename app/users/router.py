from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm

from app.core.database import get_db
from app.users import service
from app.users.schemas import UserCreate, UserOut, Token
from app.users.models import User
from app.users.dependencies import get_current_user
from app.core.security import create_access_token


router = APIRouter(prefix='/auth', tags=['auth'])

@router.post("/register", response_model=UserOut)
async def register(user_data: UserCreate, db:AsyncSession=Depends(get_db)):
    return await service.register_user(db, user_data)

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession=Depends(get_db)):
    user = await service.authenticate_user(db, form_data.username, form_data.password)
    access_token = create_access_token({'sub':user.username})
    return {'access_token':access_token, 'token_type':'bearer'}

@router.get("/me", response_model=UserOut)
async def get_me(current_user:User=Depends(get_current_user)):
    return current_user