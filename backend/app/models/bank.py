# app/models/bank.py
from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from app.models.base import TimestampModel
from app.schemas.base import TimestampResponseMixin
from pydantic import validator
from app.models.user import User

class BankBase(SQLModel):
    name: str = Field(max_length=100)
    color: str = Field(max_length=50)
    start_balance: int = Field(default=0)
    end_balance: int = Field(default=0)

    @validator('end_balance', pre=True, always=True)
    def set_end_balance(cls, v, values):
        """Set end_balance equal to start_balance if not provided"""
        if 'start_balance' in values and v == 0:
            return values['start_balance']
        return v

class Bank(BankBase, TimestampModel, table=True):
    __tablename__ = "banks"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")  # Add user relationship
    transactions: List["Transaction"] = Relationship(back_populates="bank")
    user: User = Relationship(back_populates="banks")

class BankCreate(BankBase):
    pass

class BankRead(BankBase, TimestampResponseMixin):
    id: int
    user_id: int  # Include in response

class BankUpdate(SQLModel):
    name: Optional[str] = None
    color: Optional[str] = None
    start_balance: Optional[int] = None