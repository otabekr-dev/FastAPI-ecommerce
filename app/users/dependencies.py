from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.users import repository
from app.users.models import User, Roles
from app.core.security import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/login')

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
)-> User:
    payload = decode_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate credentials'
        )

    username = payload.get('sub')

    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate credentials'
        )

    user = await repository.get_by_username(db, username)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate credentials'
        )

    return user

async def require_admin(
    current_user: User = Depends(get_current_user)
) -> User:

    if current_user.role != Roles.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='User is not Admin')
    
    return current_user