from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date, timedelta
from .. import models, schemas, crud
from ..auth import get_current_user
from ..database import get_db

router = APIRouter(
    prefix="/spending",
    tags=["Spending"]
)

# --- Spending Endpoints ---
@router.get("/", response_model=schemas.StandardResponse[List[schemas.Spending]])
def read_spendings(
    skip: int = 0, 
    limit: int = 100,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None, 
    category_id: Optional[int] = None,
    db: Session = Depends(get_db), 
    current_user: schemas.UserData = Depends(get_current_user)
):
    if start_date and end_date and start_date > end_date:
        raise HTTPException(
            status_code=400,
            detail="start_date cannot be after end_date",
        )
    today = date.today()

    if end_date is None:
        end_date = today

    if start_date is None:
        start_date = today - timedelta(days=7)
    spendings = crud.get_spendings(db, user_id=current_user.id, skip=skip, limit=limit, start_date=start_date, end_date=end_date, category_id=category_id)
    return schemas.StandardResponse(data=spendings, message="Transactions retrieved successfully")

@router.post("/", response_model=schemas.StandardResponse[schemas.Spending])
def create_spending(spending: schemas.SpendingCreate, db: Session = Depends(get_db), current_user: schemas.UserData = Depends(get_current_user)):
    new_spending = crud.create_user_spending(db=db, spending=spending, user_id=current_user.id)
    return schemas.StandardResponse(data=new_spending, message="Transaction added successfully")


@router.put("/{spending_id}", response_model=schemas.StandardResponse[schemas.Spending])
def update_spending(spending_id: int, spending: schemas.SpendingUpdate, db: Session = Depends(get_db), current_user: schemas.UserData = Depends(get_current_user)):
    updated_spending = crud.update_user_spending(db=db, spending_id=spending_id, spending=spending, user_id=current_user.id)
    return schemas.StandardResponse(data=updated_spending, message="Transaction updated successfully")

@router.delete("/{spending_id}", response_model=schemas.StandardResponse[schemas.Spending])
def delete_spending(spending_id: int, db: Session = Depends(get_db), current_user: schemas.UserData = Depends(get_current_user)):
    deleted_spending = crud.delete_user_spending(db=db, spending_id=spending_id)
    return schemas.StandardResponse(data=deleted_spending, message="Transaction deleted successfully")
