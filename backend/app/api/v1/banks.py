from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from app.db.session import get_session
from app.models.bank import Bank, BankCreate, BankRead, BankUpdate
from app.models.user import User
from app.api.deps import get_current_user
from app.core.utils import get_utc_now
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/", response_model=BankRead)
async def create_bank(
    *,
    session: Session = Depends(get_session),
    bank_in: BankCreate,
    current_user: User = Depends(get_current_user)
):
    try:
        # Create bank with current user's ID
        db_bank = Bank(
            **bank_in.dict(),
            user_id=current_user.id
        )
        
        session.add(db_bank)
        session.commit()
        session.refresh(db_bank)
        
        logger.info(f"Bank created successfully: {db_bank.id}")
        return db_bank
    except Exception as e:
        logger.error(f"Error creating bank: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error creating bank: {str(e)}"
        )

@router.get("/", response_model=List[BankRead])
async def get_banks(
    *,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100
):
    try:
        # Filter banks by current user
        query = select(Bank).where(Bank.user_id == current_user.id)
        query = query.offset(skip).limit(limit)
        banks = session.exec(query).all()
        return banks
    except Exception as e:
        logger.error(f"Error retrieving banks: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving banks: {str(e)}"
        )

@router.get("/{bank_id}", response_model=BankRead)
async def get_bank(
    *,
    session: Session = Depends(get_session),
    bank_id: int,
    current_user: User = Depends(get_current_user)
):
    try:
        bank = session.get(Bank, bank_id)
        if not bank:
            raise HTTPException(status_code=404, detail="Bank not found")
        
        # Verify bank belongs to current user
        if bank.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to access this bank")
            
        return bank
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving bank: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving bank: {str(e)}"
        )

@router.patch("/{bank_id}", response_model=BankRead)
async def update_bank(
    *,
    session: Session = Depends(get_session),
    bank_id: int,
    bank_update: BankUpdate,
    current_user: User = Depends(get_current_user)
):
    try:
        bank = session.get(Bank, bank_id)
        if not bank:
            raise HTTPException(status_code=404, detail="Bank not found")
            
        # Verify bank belongs to current user
        if bank.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to modify this bank")

        # Update bank fields
        update_data = bank_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(bank, field, value)

        bank.updated_at = get_utc_now()

        session.add(bank)
        session.commit()
        session.refresh(bank)
        
        logger.info(f"Bank updated successfully: {bank.id}")
        return bank
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating bank: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error updating bank: {str(e)}"
        )

@router.delete("/{bank_id}")
async def delete_bank(
    *,
    session: Session = Depends(get_session),
    bank_id: int,
    current_user: User = Depends(get_current_user)
):
    try:
        bank = session.get(Bank, bank_id)
        if not bank:
            raise HTTPException(status_code=404, detail="Bank not found")
            
        # Verify bank belongs to current user
        if bank.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to delete this bank")

        session.delete(bank)
        session.commit()
        
        logger.info(f"Bank deleted successfully: {bank_id}")
        return {"message": "Bank deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting bank: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error deleting bank: {str(e)}"
        )