# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from app.database import get_db
# from app.schemas.course import Course, Enrollment
# from app.services import course_service, user_service
#
# router = APIRouter()
#
#
# @router.get("/dashboard/{student_id}")
# def get_student_dashboard(student_id: int, db: Session = Depends(get_db)):
#     student = user_service.get_user(db, user_id=student_id)
#     if not student or student.role != "student":
#         raise HTTPException(status_code=404, detail="Student not found")
#
#     enrollments = course_service.get_student_enrollments(db, student_id)
#     progress = course_service.get_student_progress(db, student_id)
#     comparison = course_service.get_student_comparison(db, student_id)
#
#     return {
#         "enrollments": enrollments,
#         "progress": progress,
#         "comparison": comparison
#     }
#
#
# @router.get("/courses/{student_id}", response_model=List[Course])
# def get_student_courses(student_id: int, db: Session = Depends(get_db)):
#     return course_service.get_student_courses(db, student_id)
#
