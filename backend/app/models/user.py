from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from app.models.base import TimestampModel
from app.schemas.base import TimestampResponseMixin

class UserBase(SQLModel):
    fullname: str = Field(max_length=100)
    username: str = Field(max_length=50)
    email: str = Field(max_length=50)
    is_active: bool = Field(default=True)

class User(UserBase, TimestampModel, table=True):
    __tablename__ = "users"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    password: str = Field(max_length=255)
    
    # Add relationships
    categories: List["Category"] = Relationship(back_populates="user")
    banks: List["Bank"] = Relationship(back_populates="user")
    transactions: List["Transaction"] = Relationship(back_populates="user")

class UserCreate(UserBase):
    password: str

class UserRead(UserBase, TimestampResponseMixin):
    id: int

class UserUpdate(SQLModel):
    fullname: Optional[str] = None
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None