from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from app.models.base import TimestampModel
from app.schemas.base import TimestampResponseMixin
from app.models.user import User

class CategoryBase(SQLModel):
    name: str = Field(max_length=100)
    is_income: bool = Field(default=False)

class Category(CategoryBase, TimestampModel, table=True):
    __tablename__ = "categories"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")  # Add user relationship
    transactions: List["Transaction"] = Relationship(back_populates="category")
    user: User = Relationship(back_populates="categories")

class CategoryCreate(CategoryBase):
    pass

class CategoryRead(CategoryBase, TimestampResponseMixin):
    id: int
    user_id: int  # Include in response

class CategoryUpdate(SQLModel):
    name: Optional[str] = None
    is_income: Optional[bool] = None