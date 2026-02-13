from .. import models, schemas, crud
from fastapi import  FastAPI, Response, status, HTTPException,Depends, APIRouter
from ..database import  get_db 
from sqlalchemy.orm import Session
from typing import  List, Optional
from sqlalchemy import func
from ..auth import get_current_user


router = APIRouter(
    prefix="/categories",
    tags=['categories']
)
# --- Category Endpoints ---
@router.get("/", response_model=schemas.StandardResponse[List[schemas.Category]])
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: schemas.UserData = Depends(get_current_user)):
    categories = crud.get_categories(db, user_id=current_user.id, skip=skip, limit=limit)
    return schemas.StandardResponse(data=categories, message="Categories retrieved successfully")

@router.post("/", response_model=schemas.StandardResponse[schemas.Category])
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db), current_user: schemas.UserData = Depends(get_current_user)):
    new_category = crud.create_user_category(db=db, category=category, user_id=current_user.id)
    return schemas.StandardResponse(data=new_category, message="Category created successfully")
