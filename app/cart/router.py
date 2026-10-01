from fastapi import APIRouter, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.users.dependencies import require_admin
from app.cart import service
from app.cart.schemas import CartItemUpdate, CartItemOut, CartOut, CartItemAdd