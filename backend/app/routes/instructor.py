from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
# from app.schemas.course_schema import CourseCreate, Course
# from app.services import course_service, user_service

router = APIRouter()


# @router.get("/dashboard/{instructor_id}")
# def get_instructor_dashboard(instructor_id: int, db: Session = Depends(get_db)):
#     instructor = user_service.get_user(db, user_id=instructor_id)
#     if not instructor or instructor.role != "instructor":
#         raise HTTPException(status_code=404, detail="Instructor not found")
#
#     courses = course_service.get_instructor_courses(db, instructor_id)
#     student_progress = course_service.get_all_students_progress(db, instructor_id)
#
#     return {
#         "courses": courses,
#         "student_progress": student_progress
#     }


# @router.post("/courses", response_model=Course)
# def create_course(course: CourseCreate, db: Session = Depends(get_db)):
#     return course_service.create_course(db, course)


# @router.get("/courses/{instructor_id}", response_model=List[Course])
# def get_instructor_courses(instructor_id: int, db: Session = Depends(get_db)):
#     return course_service.get_instructor_courses(db, instructor_id)
