from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import app.services.enrollment_services as enrollment_service
import app.schemas.schema as schemas
from ..database import get_db

router = APIRouter()

@router.post("/enrollments/")
def enroll_student(student_id: int, course_id: int, db: Session = Depends(get_db)):
    return enrollment_service.enroll_student(db, student_id, course_id)

@router.get("/enrollments/student/{student_id}")
def get_student_enrollments(student_id: int, db: Session = Depends(get_db)):
    return enrollment_service.get_student_enrollments(db, student_id)
