from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from datetime import date
from app.db.session import get_session
from app.models.transaction import Transaction, TransactionCreate, TransactionRead, TransactionUpdate
from app.models.bank import Bank
from app.models.category import Category
from app.models.user import User
from app.api.deps import get_current_user
from app.core.utils import get_utc_now
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/", response_model=TransactionRead)
async def create_transaction(
    *,
    session: Session = Depends(get_session),
    transaction_in: TransactionCreate,
    current_user: User = Depends(get_current_user)
):
    try:
        # Verify category exists
        category = session.get(Category, transaction_in.category_id)
        if not category:
            raise HTTPException(
                status_code=404,
                detail="Category not found"
            )

        # Verify bank exists
        bank = session.get(Bank, transaction_in.bank_id)
        if not bank:
            raise HTTPException(
                status_code=404,
                detail="Bank not found"
            )

        # Create transaction with current user's ID
        db_transaction = Transaction(
            **transaction_in.dict(),
            user_id=current_user.id  # Set user_id dari current_user
        )

        # Update bank balance
        if category.is_income:
            bank.end_balance += transaction_in.amount
        else:
            bank.end_balance -= transaction_in.amount
        
        bank.updated_at = get_utc_now()
        
        session.add(db_transaction)
        session.add(bank)
        session.commit()
        session.refresh(db_transaction)
        
        logger.info(f"Transaction created successfully: {db_transaction.id}")
        return db_transaction
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating transaction: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error creating transaction: {str(e)}"
        )

@router.get("/", response_model=List[TransactionRead])
async def get_transactions(
    *,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100,
    start_date: date = None,
    end_date: date = None,
    category_id: int = None,
    bank_id: int = None
):
    try:
        # Start with base query filtering by current user
        query = select(Transaction).where(Transaction.user_id == current_user.id)

        if start_date:
            query = query.where(Transaction.date >= start_date)
        if end_date:
            query = query.where(Transaction.date <= end_date)
        if category_id:
            query = query.where(Transaction.category_id == category_id)
        if bank_id:
            query = query.where(Transaction.bank_id == bank_id)

        query = query.offset(skip).limit(limit).order_by(Transaction.date.desc())
        transactions = session.exec(query).all()
        return transactions
    except Exception as e:
        logger.error(f"Error retrieving transactions: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving transactions: {str(e)}"
        )

@router.get("/{transaction_id}", response_model=TransactionRead)
async def get_transaction(
    *,
    session: Session = Depends(get_session),
    transaction_id: int,
    current_user: User = Depends(get_current_user)
):
    try:
        transaction = session.get(Transaction, transaction_id)
        if not transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")
        
        # Verify transaction belongs to current user
        if transaction.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to access this transaction")
            
        return transaction
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving transaction: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving transaction: {str(e)}"
        )

@router.patch("/{transaction_id}", response_model=TransactionRead)
async def update_transaction(
    *,
    session: Session = Depends(get_session),
    transaction_id: int,
    transaction_update: TransactionUpdate,
    current_user: User = Depends(get_current_user)
):
    try:
        transaction = session.get(Transaction, transaction_id)
        if not transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")

        update_data = transaction_update.dict(exclude_unset=True)

        # If updating amount or bank, adjust bank balances
        if "amount" in update_data or "bank_id" in update_data:
            old_bank = session.get(Bank, transaction.bank_id)
            new_bank = old_bank

            if "bank_id" in update_data:
                new_bank = session.get(Bank, update_data["bank_id"])
                if not new_bank:
                    raise HTTPException(status_code=404, detail="New bank not found")

            # Reverse old transaction
            if transaction.category.is_income:
                old_bank.end_balance -= transaction.amount
            else:
                old_bank.end_balance += transaction.amount

            # Apply new transaction
            new_amount = update_data.get("amount", transaction.amount)
            if transaction.category.is_income:
                new_bank.end_balance += new_amount
            else:
                new_bank.end_balance -= new_amount

            old_bank.updated_at = get_utc_now()
            new_bank.updated_at = get_utc_now()

            session.add(old_bank)
            if new_bank != old_bank:
                session.add(new_bank)

        # Update transaction fields
        for field, value in update_data.items():
            setattr(transaction, field, value)

        transaction.updated_at = get_utc_now()

        session.add(transaction)
        session.commit()
        session.refresh(transaction)
        
        logger.info(f"Transaction updated successfully: {transaction.id}")
        return transaction
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating transaction: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error updating transaction: {str(e)}"
        )

@router.delete("/{transaction_id}")
async def delete_transaction(
    *,
    session: Session = Depends(get_session),
    transaction_id: int,
    current_user: User = Depends(get_current_user)
):
    try:
        transaction = session.get(Transaction, transaction_id)
        if not transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")

        # Adjust bank balance
        bank = session.get(Bank, transaction.bank_id)
        if transaction.category.is_income:
            bank.end_balance -= transaction.amount
        else:
            bank.end_balance += transaction.amount

        bank.updated_at = get_utc_now()

        session.delete(transaction)
        session.add(bank)
        session.commit()
        
        logger.info(f"Transaction deleted successfully: {transaction_id}")
        return {"message": "Transaction deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting transaction: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error deleting transaction: {str(e)}"
        )