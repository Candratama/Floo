from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from datetime import datetime, timedelta
import pytz
import logging
from app.core.security import verify_password, create_access_token, get_password_hash
from app.db.session import get_session
from app.models.user import User, UserCreate, UserRead
from app.core.config import settings

router = APIRouter()
logger = logging.getLogger(__name__)

jakarta_tz = pytz.timezone('Asia/Jakarta')

@router.post("/register", response_model=UserRead)
async def register(
    *, 
    session: Session = Depends(get_session), 
    user_in: UserCreate
):
    try:
        # Check username
        user = session.exec(
            select(User).where(User.username == user_in.username)
        ).first()
        if user:
            raise HTTPException(
                status_code=400,
                detail="Username already registered"
            )
        
        # Check email
        user = session.exec(
            select(User).where(User.email == user_in.email)
        ).first()
        if user:
            raise HTTPException(
                status_code=400,
                detail="Email already registered"
            )
        
        current_time = datetime.now(jakarta_tz)
        
        # Create new user
        db_user = User(
            fullname=user_in.fullname,
            username=user_in.username,
            email=user_in.email,
            password=get_password_hash(user_in.password),
            created_at=current_time,
            updated_at=current_time
        )
        
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        
        logger.info(f"User registered successfully: {user_in.username}")
        return db_user
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during registration: {str(e)}"
        )

@router.post("/login", response_model=dict)
async def login(
    session: Session = Depends(get_session),
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    try:
        user = session.exec(
            select(User).where(User.username == form_data.username)
        ).first()
        
        if not user or not verify_password(form_data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Inactive user"
            )
        
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(user.id)}, 
            expires_delta=access_token_expires
        )
        
        logger.info(f"User logged in successfully: {form_data.username}")
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during login: {str(e)}"
        )