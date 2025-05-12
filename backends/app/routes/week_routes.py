from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import app.schemas.schema as schema
import app.services.week_services as week_service
from ..database import get_db

router = APIRouter()

@router.post("/weeks/")
def create_week(course_id: int, week_number: int, db: Session = Depends(get_db)):
    return week_service.create_week(db, course_id, week_number)

@router.get("/weeks/{week_id}")
def get_week(week_id: int, db: Session = Depends(get_db)):
    return week_service.get_week(db, week_id)
