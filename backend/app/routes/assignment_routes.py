from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import app.services.assignment_services as assignment_service
from ..database import get_db

router = APIRouter()

@router.post("/assignments/")
def create_assignment(week_id: int, title: str, type: str, db: Session = Depends(get_db)):
    return assignment_service.create_assignment(db, week_id, title, type)

@router.get("/assignments/{assessment_id}")
def get_assignment(assessment_id: int, db: Session = Depends(get_db)):
    return assignment_service.get_assignment(db, assessment_id)

@router.get("/assignments/week/{week_id}")
def get_week_assignments(week_id: int, db: Session = Depends(get_db)):
    return assignment_service.get_week_assignments(db, week_id)
