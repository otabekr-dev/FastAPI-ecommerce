import enum
from sqlalchemy import String, DateTime, Enum
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func
from app.core.database import Base

class Roles(str, enum.Enum):
    ADMIN = 'ADMIN'
    CUSTOMER = 'CUSTOMER'


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    role: Mapped[Roles] = mapped_column(Enum(Roles), default=Roles.CUSTOMER)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
