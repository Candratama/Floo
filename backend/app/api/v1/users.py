from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from app.db.session import get_session
from app.models.user import User, UserCreate, UserRead, UserUpdate
from app.api.deps import get_current_user
from app.core.security import get_password_hash
from app.core.utils import get_utc_now
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/", response_model=List[UserRead])
async def get_users(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    try:
        users = session.exec(
            select(User)
            .offset(skip)
            .limit(limit)
        ).all()
        return users
    except Exception as e:
        logger.error(f"Error retrieving users: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving users: {str(e)}"
        )

@router.get("/me", response_model=UserRead)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    return current_user

@router.patch("/me", response_model=UserRead)
async def update_user_me(
    *,
    session: Session = Depends(get_session),
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user)
):
    try:
        update_data = user_update.dict(exclude_unset=True)

        if "username" in update_data:
            existing_user = session.exec(
                select(User)
                .where(User.username == update_data["username"])
                .where(User.id != current_user.id)
            ).first()
            if existing_user:
                raise HTTPException(
                    status_code=400,
                    detail="Username already registered"
                )

        if "email" in update_data:
            existing_user = session.exec(
                select(User)
                .where(User.email == update_data["email"])
                .where(User.id != current_user.id)
            ).first()
            if existing_user:
                raise HTTPException(
                    status_code=400,
                    detail="Email already registered"
                )

        if "password" in update_data:
            update_data["password"] = get_password_hash(update_data["password"])

        for field, value in update_data.items():
            setattr(current_user, field, value)

        current_user.updated_at = get_utc_now()

        session.add(current_user)
        session.commit()
        session.refresh(current_user)
        
        return current_user

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating user: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error updating user: {str(e)}"
        )

@router.get("/{user_id}", response_model=UserRead)
async def get_user(
    user_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    try:
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving user: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving user: {str(e)}"
        )