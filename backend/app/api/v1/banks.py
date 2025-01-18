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
        # Check if bank with same name exists
        existing_bank = session.exec(
            select(Bank).where(Bank.name == bank_in.name)
        ).first()
        if existing_bank:
            raise HTTPException(
                status_code=400,
                detail="Bank with this name already exists"
            )

        # Create bank with end_balance equal to start_balance
        db_bank = Bank(
            name=bank_in.name,
            color=bank_in.color,
            start_balance=bank_in.start_balance,
            end_balance=bank_in.start_balance  # Set end_balance sama dengan start_balance
        )
        
        session.add(db_bank)
        session.commit()
        session.refresh(db_bank)
        
        logger.info(f"Bank account created successfully: {bank_in.name}")
        return db_bank
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating bank account: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error creating bank account: {str(e)}"
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
        banks = session.exec(
            select(Bank)
            .offset(skip)
            .limit(limit)
        ).all()
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

        update_data = bank_update.dict(exclude_unset=True)

        if "name" in update_data:
            existing_bank = session.exec(
                select(Bank)
                .where(Bank.name == update_data["name"])
                .where(Bank.id != bank_id)
            ).first()
            if existing_bank:
                raise HTTPException(
                    status_code=400,
                    detail="Bank with this name already exists"
                )

        for field, value in update_data.items():
            setattr(bank, field, value)

        bank.updated_at = get_utc_now()

        session.add(bank)
        session.commit()
        session.refresh(bank)
        
        logger.info(f"Bank account updated successfully: {bank.name}")
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

        session.delete(bank)
        session.commit()
        
        logger.info(f"Bank account deleted successfully: {bank.name}")
        return {"message": "Bank deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting bank: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error deleting bank: {str(e)}"
        )