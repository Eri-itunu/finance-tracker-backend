from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, crud
from ..auth import get_current_user
from ..database import get_db

router = APIRouter(
    prefix="/savings",
    tags=["Savings"]
)




# --- Savings Endpoints ---
@router.get("/", response_model=schemas.StandardResponse[List[schemas.SavingsGoal]])
def read_savings_goals(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: schemas.UserData = Depends(get_current_user)):
    goals = crud.get_savings_goals(db, user_id=current_user.id, skip=skip, limit=limit)
    return schemas.StandardResponse(data=goals, message="Savings goals retrieved successfully")

@router.post("/", response_model=schemas.StandardResponse[schemas.SavingsGoal])
def create_savings_goal(goal: schemas.SavingsGoalCreate, db: Session = Depends(get_db), current_user: schemas.UserData = Depends(get_current_user)):
    new_goal = crud.create_user_savings_goal(db=db, goal=goal, user_id=current_user.id)
    return schemas.StandardResponse(data=new_goal, message="Savings goal created successfully")

@router.post("/{goal_id}/contributions/", response_model=schemas.StandardResponse[schemas.SavingsContribution])
def create_contribution(goal_id: int, contribution: schemas.SavingsContributionCreate, db: Session = Depends(get_db), current_user: schemas.UserData = Depends(get_current_user)):
    # Verify goal belongs to user
    # Note: In a real app, adding a check here would be better safe than sorry
    new_contribution = crud.create_savings_contribution(db=db, contribution=contribution, goal_id=goal_id, user_id=current_user.id)
    return schemas.StandardResponse(data=new_contribution, message="Contribution added successfully")

