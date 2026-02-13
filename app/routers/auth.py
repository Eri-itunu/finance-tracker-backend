from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from .. import schemas
from ..crud import get_password_hash, verify_password
from ..auth import create_access_token
import logging

from app.exceptions import UserAlreadyExistsException, DatabaseException

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/register", response_model=schemas.AuthResponse, status_code=status.HTTP_201_CREATED)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):

    try:
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == user.email).first()
        if existing_user:
            raise UserAlreadyExistsException(email=user.email)
        
        # Hash password
        hashed_password = get_password_hash(user.password)
        
        # Create user object
        db_user = User(
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            default_currency=user.default_currency,
            password=hashed_password
        )
        
        # Save to database
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        logger.info(f"User registered successfully: {user.email}")
        
    except UserAlreadyExistsException:
        # Re-raise custom exceptions
        raise
        
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Integrity error during registration: {str(e)}")
        # This catches race conditions
        raise UserAlreadyExistsException(email=user.email)
        
    except OperationalError as e:
        db.rollback()
        logger.error(f"Database connection error: {str(e)}")
        raise DatabaseException("Unable to connect to database. Please try again later.")
        
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error during registration: {str(e)}", exc_info=True)
        raise DatabaseException("Registration failed. Please try again later.")
    
    # Generate access token
    try:
        access_token = create_access_token(data={"sub": db_user.email})
    except Exception as e:
        logger.error(f"Token creation failed: {str(e)}", exc_info=True)
        raise DatabaseException("Failed to create authentication token")
    
    user_data = schemas.UserData.model_validate(db_user)
    auth_data = schemas.AuthData(
            user=user_data,
            access_token=access_token,
            token_type="bearer"
        )
        
    return schemas.AuthResponse(
        success=True,
        data=auth_data,
        message="User registered successfully"
    )







@router.post("/login",response_model=schemas.AuthResponse)
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    access_token = create_access_token(data={"sub": db_user.email})
    return schemas.AuthResponse(
        success=True,
        data=schemas.AuthData(
            user=schemas.UserData.model_validate(db_user),
            access_token=access_token,
            token_type="bearer"
        ),
        message="User logged in successfully"
    )