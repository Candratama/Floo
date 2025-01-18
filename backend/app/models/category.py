from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from app.models.base import TimestampModel
from app.schemas.base import TimestampResponseMixin

class CategoryBase(SQLModel):
    name: str = Field(max_length=100)
    is_income: bool = Field(default=False)

class Category(CategoryBase, TimestampModel, table=True):
    __tablename__ = "categories"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    transactions: List["Transaction"] = Relationship(back_populates="category")

class CategoryCreate(CategoryBase):
    pass

class CategoryRead(CategoryBase, TimestampResponseMixin):
    id: int

class CategoryUpdate(SQLModel):
    name: Optional[str] = None
    is_income: Optional[bool] = None