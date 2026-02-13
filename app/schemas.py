from pydantic import BaseModel, EmailStr, validator
from typing import Optional, Any,List
from datetime import datetime
from enum import Enum


class Currency(str, Enum):
    """Supported currencies"""
    NGN = 'NGN'  # Nigerian Naira
    GBP = 'GBP'  # British Pound
    USD = 'USD'  # US Dollar
    EUR = 'EUR'  # Euro


class ErrorDetail(BaseModel):
    """Error details structure"""
    message: str
    status_code: int
    details: Optional[Any] = None


class ErrorResponse(BaseModel):
    """Standard error response format"""
    success: bool = False
    error: ErrorDetail


class SuccessResponse(BaseModel):
    """Generic success response wrapper"""
    success: bool = True
    data: Any
    message: Optional[str] = None

from typing import Generic, TypeVar
T = TypeVar('T')

class StandardResponse(BaseModel, Generic[T]):
    """Standardized response wrapper"""
    success: bool = True
    data: Optional[T] = None
    message: Optional[str] = None


class UserCreate(BaseModel):
    """Schema for user registration"""
    email: EmailStr
    first_name: str
    last_name: str
    default_currency: Currency
    password: str
    



class UserLogin(BaseModel):
    """Schema for user login"""
    email: EmailStr
    password: str


class UserData(BaseModel):
    """User data returned in responses (no sensitive info)"""
    id: int
    email: EmailStr
    first_name: Optional[str]
    last_name: Optional[str]
    default_currency: Optional[Currency]
    created_at: datetime
    
    class Config:
        from_attributes = True  # Allows creation from ORM models

class AuthData(BaseModel):
    """Authentication response data structure"""
    user: UserData
    access_token: str
    token_type: str = "bearer"


class AuthResponse(BaseModel):
    """Complete authentication response (register/login)"""
    success: bool = True
    data: AuthData
    message: Optional[str] = "Authentication successful"


class UserProfileResponse(BaseModel):
    """Response for getting user profile (no token)"""
    success: bool = True
    data: UserData
    message: Optional[str] = None


class UserUpdateRequest(BaseModel):
    """Schema for updating user profile"""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    default_currency: Optional[Currency] = None
    

class PasswordChangeRequest(BaseModel):
    """Schema for changing password"""
    current_password: str
    new_password: str
  


class MessageResponse(BaseModel):
    """Simple message response"""
    success: bool = True
    message: str

# --- Auth Schemas ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# --- Category Schemas ---
class CategoryBase(BaseModel):
    category_name: str
    # type and icon removed in model
    # is_deleted added
    is_deleted: bool = False

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True

# --- Income Schemas ---
class IncomeBase(BaseModel):
    amount: float
    source: str
    type: Optional[str] = None 
    date: Optional[datetime] = None


class IncomeCreate(IncomeBase):
    pass

class Income(IncomeBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True

# --- Spending Schemas ---
class SpendingBase(BaseModel):
    amount: float
    notes: Optional[str] = None # description -> notes
    item_name: Optional[str] = None # added
    date: Optional[datetime] = None
    category_id: Optional[int] = None # This is still in Spending model (line 55)
    is_deleted: bool = False

class SpendingCreate(SpendingBase):
    pass

class SpendingUpdate(SpendingBase):
    id: int
    pass

class Spending(SpendingBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True

# --- Savings Schemas ---
class SavingsContributionBase(BaseModel):
    amount: float
    date: Optional[datetime] = None

class SavingsContributionCreate(SavingsContributionBase):
    pass

class SavingsContribution(SavingsContributionBase):
    id: int
    goal_id: int
    user_id: Optional[int] = None

    class Config:
        from_attributes = True

class SavingsGoalBase(BaseModel):
    goal_name: str # title -> goal_name
    target_amount: float
    deadline: Optional[datetime] = None
    # current_amount removed from model

class SavingsGoalCreate(SavingsGoalBase):
    pass

class SavingsGoal(SavingsGoalBase):
    id: int
    user_id: int
    created_at: datetime
    # contributions -> savings_contributions in model
    savings_contributions: List[SavingsContribution] = []

    class Config:
        from_attributes = True
