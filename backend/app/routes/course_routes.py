from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import app.services.course_services as service
from app.schemas.schema import CourseCreate
from ..database import get_db

router = APIRouter()

@router.get("/courses/{course_id}")
def get_course(course_id: int, db: Session = Depends(get_db)):
    return service.get_course(db, course_id)

@router.get("/courses/")
def get_courses(db: Session = Depends(get_db)):
    return service.get_courses(db)

@router.post("/courses/")
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    return service.create_course(db, course)

@router.get("/courses/instructor/{instructor_id}")
def get_instructor_courses(instructor_id: int, db: Session = Depends(get_db)):
    return service.get_instructor_courses(db, instructor_id)
