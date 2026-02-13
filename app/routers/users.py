from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import crud, schemas
from ..auth import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/me/", response_model=schemas.StandardResponse[schemas.UserData])
async def read_users_me(current_user: schemas.UserData = Depends(get_current_user)):
    return schemas.StandardResponse(data=current_user, message="User profile retrieved successfully")

@router.post("/", response_model=schemas.StandardResponse[schemas.UserData])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = crud.create_user(db=db, user=user)
    return schemas.StandardResponse(data=new_user, message="User created successfully")
