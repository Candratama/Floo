from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from app.db.session import get_session
from app.models.category import Category, CategoryCreate, CategoryRead, CategoryUpdate
from app.models.user import User
from app.api.deps import get_current_user
from app.core.utils import get_utc_now
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/", response_model=CategoryRead)
async def create_category(
    *,
    session: Session = Depends(get_session),
    category_in: CategoryCreate,
    current_user: User = Depends(get_current_user)
):
    try:
        # Create category with current user's ID
        db_category = Category(
            **category_in.dict(),
            user_id=current_user.id
        )
        
        session.add(db_category)
        session.commit()
        session.refresh(db_category)
        
        logger.info(f"Category created successfully: {db_category.id}")
        return db_category
    except Exception as e:
        logger.error(f"Error creating category: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error creating category: {str(e)}"
        )

@router.get("/", response_model=List[CategoryRead])
async def get_categories(
    *,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100
):
    try:
        # Filter categories by current user
        query = select(Category).where(Category.user_id == current_user.id)
        query = query.offset(skip).limit(limit)
        categories = session.exec(query).all()
        return categories
    except Exception as e:
        logger.error(f"Error retrieving categories: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving categories: {str(e)}"
        )

@router.get("/{category_id}", response_model=CategoryRead)
async def get_category(
    *,
    session: Session = Depends(get_session),
    category_id: int,
    current_user: User = Depends(get_current_user)
):
    try:
        category = session.get(Category, category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        
        # Verify category belongs to current user
        if category.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to access this category")
            
        return category
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving category: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving category: {str(e)}"
        )

@router.patch("/{category_id}", response_model=CategoryRead)
async def update_category(
    *,
    session: Session = Depends(get_session),
    category_id: int,
    category_update: CategoryUpdate,
    current_user: User = Depends(get_current_user)
):
    try:
        category = session.get(Category, category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
            
        # Verify category belongs to current user
        if category.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to modify this category")

        # Update category fields
        update_data = category_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(category, field, value)

        category.updated_at = get_utc_now()

        session.add(category)
        session.commit()
        session.refresh(category)
        
        logger.info(f"Category updated successfully: {category.id}")
        return category
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating category: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error updating category: {str(e)}"
        )

@router.delete("/{category_id}")
async def delete_category(
    *,
    session: Session = Depends(get_session),
    category_id: int,
    current_user: User = Depends(get_current_user)
):
    try:
        category = session.get(Category, category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
            
        # Verify category belongs to current user
        if category.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to delete this category")

        session.delete(category)
        session.commit()
        
        logger.info(f"Category deleted successfully: {category_id}")
        return {"message": "Category deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting category: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error deleting category: {str(e)}"
        )