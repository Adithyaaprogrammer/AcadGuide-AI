from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import app.services.submission_services as submission_service
from ..database import get_db

router = APIRouter()

@router.post("/submissions/")
def create_submission(assessment_id: int, student_id: int, content: str, db: Session = Depends(get_db)):
    return submission_service.create_submission(db, assessment_id, student_id, content)

@router.post("/submissions/grade")
def grade_submission(submission_id: int, grade: int, db: Session = Depends(get_db)):
    return submission_service.grade_submission(db, submission_id, grade)

@router.get("/submissions/student/{student_id}")
def get_student_submissions(student_id: int, assessment_id: int, db: Session = Depends(get_db)):
    return submission_service.get_student_submissions(db, student_id, assessment_id)
