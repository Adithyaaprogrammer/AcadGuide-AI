from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import app.services.user_services as service
from app.schemas.user_schema import UserCreate, UserResponse
from app.database import get_db
from fastapi.security import HTTPBasic, HTTPBasicCredentials

router = APIRouter()
security = HTTPBasic()

@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/users/email/{email}", response_model=UserResponse)
def get_user_by_email(email: str, db: Session = Depends(get_db)):
    user = service.get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/users/", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    return service.create_user(db, user)

@router.post("/users/authenticate", response_model=UserResponse)
def authenticate_user(credentials: HTTPBasicCredentials = Depends(security), db: Session = Depends(get_db)):
    return service.authenticate_user(db, credentials.username, credentials.password)
