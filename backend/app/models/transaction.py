# app/models/transaction.py
from datetime import datetime, date
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from app.models.base import TimestampModel
from app.schemas.base import TimestampResponseMixin
from app.models.category import Category
from app.models.bank import Bank
from app.models.user import User

class TransactionBase(SQLModel):
    date: date
    amount: int
    description: str = Field(max_length=255)
    category_id: int = Field(foreign_key="categories.id")
    bank_id: int = Field(foreign_key="banks.id")

# Base model untuk database dengan user_id
class Transaction(TransactionBase, TimestampModel, table=True):
    __tablename__ = "transactions"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")  # Required di database
    category: Category = Relationship(back_populates="transactions")
    bank: Bank = Relationship(back_populates="transactions")
    user: User = Relationship()

# Model untuk create request (tanpa user_id)
class TransactionCreate(TransactionBase):
    pass

class TransactionRead(TransactionBase, TimestampResponseMixin):
    id: int
    user_id: int  # Include in response

class TransactionUpdate(SQLModel):
    date: Optional[date] = None
    amount: Optional[int] = None
    description: Optional[str] = None
    category_id: Optional[int] = None
    bank_id: Optional[int] = None