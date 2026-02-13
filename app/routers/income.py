from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, crud
from ..auth import get_current_user
from ..database import get_db

router = APIRouter(
    prefix="/income",
    tags=["Income"]
)

# --- Income Endpoints ---
@router.get("/", response_model=schemas.StandardResponse[List[schemas.Income]])
def read_incomes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: schemas.UserData = Depends(get_current_user)):
    incomes = crud.get_incomes(db, user_id=current_user.id, skip=skip, limit=limit)
    return schemas.StandardResponse(data=incomes, message="Incomes retrieved successfully")

@router.post("/", response_model=schemas.StandardResponse[schemas.Income])
def create_income(income: schemas.IncomeCreate, db: Session = Depends(get_db), current_user: schemas.UserData = Depends(get_current_user)):
    new_income = crud.create_user_income(db=db, income=income, user_id=current_user.id)
    return schemas.StandardResponse(data=new_income, message="Income added successfully")