from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user_model import User, UserType
from app.models.models import Course, Enrollment, Submission
from app.schemas.instructor_dashboard_schema import InstructorDashboardResponse
from app.services.user_services import get_current_user

router = APIRouter()

from statistics import median

@router.get("/instructor_dashboard", response_model=InstructorDashboardResponse)
def get_instructor_dashboard(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role != UserType.instructor:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access forbidden")

    courses = db.query(Course).filter(Course.instructor_id == current_user.id).all()
    courses_progress = []
    for course in courses:
        enrollments = db.query(Enrollment).filter(Enrollment.course_id == course.id).all()
        student_progress_list = [calculate_student_progress(enrollment, db) for enrollment in enrollments]
        average_progress, median_progress = calculate_average_and_median_progress(course.id, db)
        courses_progress.append({
            "course_name": course.title,
            "average_progress": average_progress,
            "median_progress": median_progress,
            "student_progress_list": student_progress_list
        })

    return {"courses_progress": courses_progress}

def calculate_student_progress(enrollment: Enrollment, db: Session):
    submissions = db.query(Submission).filter(Submission.student_id == enrollment.student_id, Submission.assessment_id == enrollment.course_id).all()
    if not submissions:
        return 0
    total_score = sum(submission.grade for submission in submissions if submission.grade is not None)
    return total_score / len(submissions)

def calculate_average_and_median_progress(course_id: int, db: Session):
    submissions = db.query(Submission).join(Enrollment, Submission.student_id == Enrollment.student_id).filter(Enrollment.course_id == course_id).all()
    if not submissions:
        return 0, 0
    grades = [submission.grade for submission in submissions if submission.grade is not None]
    average_progress = sum(grades) / len(grades) if grades else 0
    median_progress = median(grades) if grades else 0
    return average_progress, median_progress