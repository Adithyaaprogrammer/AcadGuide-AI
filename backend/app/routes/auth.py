from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user_schema import UserCreate, User, UserForm
from app.services import user_services

router = APIRouter()

@router.post("/register", response_model=User)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = user_services.get_user_by_email(db, email=user.email)
    print(f"db_user: {db_user}")
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user_services.create_user(db=db, user=user)

@router.post("/login")
async def login(response: Response, form_data: UserForm, db: Session = Depends(get_db)):
    user = user_services.authenticate_user(db, form_data.email, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    response.set_cookie(key="session", value=user.username)
    return {"message": "Login successful"}


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("session")
    return {"message": "Logout successful"}