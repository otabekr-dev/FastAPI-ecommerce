from pydantic import BaseModel, ConfigDict, Field
from app.users.models import Roles
from datetime import datetime

class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=72)


class UserOut(BaseModel):
    id: int
    username: str
    role: Roles
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'