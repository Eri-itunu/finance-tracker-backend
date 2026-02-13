from sqlalchemy.orm import Session
from . import models, schemas
from sqlalchemy import func
from passlib.context import CryptContext
from typing import Optional
from datetime import date   
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    if len(plain_password.encode('utf-8')) > 72:
        print("WARNING: Password provided is > 72 bytes. This will fail with bcrypt. Truncating for check (or returning False).")
        return False
        
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        print(f"Error verifying password: {e}")
        return False

def get_password_hash(password):
    return pwd_context.hash(password)

# --- User ---
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password_val = get_password_hash(user.password)
    db_user = models.User(
        email=user.email, 
        password=hashed_password_val, 
        first_name=user.first_name, 
        last_name=user.last_name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- Categories ---
def get_categories(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Category).filter(models.Category.user_id == user_id, models.Category.is_deleted == False).offset(skip).limit(limit).all()

def create_user_category(db: Session, category: schemas.CategoryCreate, user_id: int):
    db_category = models.Category(
        category_name=category.category_name,
        user_id=user_id,
        is_deleted=category.is_deleted
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

# --- Income ---
def get_incomes(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Income).filter(models.Income.user_id == user_id).offset(skip).limit(limit).all()

def create_user_income(db: Session, income: schemas.IncomeCreate, user_id: int):
    # category_id removed from Income model
    db_income = models.Income(
        amount=income.amount, 
        source=income.source, 
        type=income.type,
        date=income.date,
        user_id=user_id
    )
    db.add(db_income)
    db.commit()
    db.refresh(db_income)
    return db_income

# --- Spending ---
def get_spendings(db: Session, user_id: int, skip: int = 0, limit: int = 100, start_date: Optional[date] = None,
    end_date: Optional[date] = None, category_id: Optional[int] = None):
    query = db.query(models.Spending).filter(models.Spending.user_id == user_id, models.Spending.is_deleted == False)
    if start_date:
        query = query.filter(func.date(models.Spending.date) >= start_date)
    if end_date:
        query = query.filter(func.date(models.Spending.date) <= end_date)
    if category_id:
        query = query.filter(models.Spending.category_id == category_id)
    return query.offset(skip).limit(limit).all()

def create_user_spending(db: Session, spending: schemas.SpendingCreate, user_id: int):
    # description -> notes, added item_name, is_deleted
    db_spending = models.Spending(
        amount=spending.amount,
        notes=spending.notes,
        item_name=spending.item_name,
        date=spending.date,
        category_id=spending.category_id,
        is_deleted=spending.is_deleted,
        user_id=user_id
    )
    db.add(db_spending)
    db.commit()
    db.refresh(db_spending)
    return db_spending

def delete_user_spending(db: Session, spending_id: int):
    db.query(models.Spending).filter(models.Spending.id == spending_id).update({"is_deleted": True})
    db.commit()
    return True

# --- Savings ---
def get_savings_goals(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.SavingsGoal).filter(models.SavingsGoal.user_id == user_id).offset(skip).limit(limit).all()

def create_user_savings_goal(db: Session, goal: schemas.SavingsGoalCreate, user_id: int):
    # title -> goal_name, current_amount removed
    db_goal = models.SavingsGoal(
        goal_name=goal.goal_name,
        target_amount=goal.target_amount,
        deadline=goal.deadline,
        user_id=user_id
    )
    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)
    return db_goal

def create_savings_contribution(db: Session, contribution: schemas.SavingsContributionCreate, goal_id: int, user_id: int):
    # Retrieve goal to check existence (current_amount removed so no update needed there? Wait, if current_amount is gone, do we compute it dynamically? Probably.)
    goal = db.query(models.SavingsGoal).filter(models.SavingsGoal.id == goal_id).first()
    if not goal:
        return None
    
    # user_id added to contribution
    db_contribution = models.SavingsContribution(
        amount=contribution.amount,
        date=contribution.date,
        goal_id=goal_id,
        user_id=user_id
    )
    db.add(db_contribution)
    db.commit()
    db.refresh(db_contribution)
    return db_contribution
