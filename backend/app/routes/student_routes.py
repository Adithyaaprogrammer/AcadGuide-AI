from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user_model import User, UserType
from app.models.models import Course, Enrollment, Submission
from app.schemas.student_dashboard_schema import StudentDashboardResponse
from app.services.user_services import get_current_user

router = APIRouter()

from statistics import median

# @router.get("/dashboard", response_model=StudentDashboardResponse)
# def get_student_dashboard(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
#     # if (current_user.role != UserType.student):
#     #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access forbidden")
#
#     enrollments = db.query(Enrollment).filter(Enrollment.student_id == current_user.id).all()
#     subjects_progress = []
#     for enrollment in enrollments:
#         course = db.query(Course).filter(Course.id == enrollment.course_id).first()
#         student_progress = calculate_student_progress(enrollment, db)
#         average_progress, median_progress = calculate_average_and_median_progress(course.id, db)
#         subjects_progress.append({
#             "course_name": course.title,
#             "student_progress": student_progress,
#             "average_progress": average_progress,
#             "median_progress": median_progress
#         })
#
#     return {"subjects_progress": subjects_progress}

@router.get("/dashboard", response_model=StudentDashboardResponse)
def get_student_dashboard():
    return {
        "subjects_progress": [
            {
                "course_name": "DSA",
                "student_progress": 78,
                "average_progress": 70,
                "median_progress": 72
            },
            {
                "course_name": "SC",
                "student_progress": 85,
                "average_progress": 77,
                "median_progress": 79
            },
            {
                "course_name": "Python",
                "student_progress": 65,
                "average_progress": 60,
                "median_progress": 62
            },
            {
                "course_name": "Java",
                "student_progress": 90,
                "average_progress": 80,
                "median_progress": 85
            }
        ]
    }

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