from sqlalchemy.orm import Session
import app.models.models as models

def enroll_student(db: Session, student_id: int, course_id: int):
    db_enrollment = models.Enrollment(student_id=student_id, course_id=course_id)
    db.add(db_enrollment)
    db.commit()
    db.refresh(db_enrollment)
    return db_enrollment

def get_student_enrollments(db: Session, student_id: int):
    return db.query(models.Enrollment).filter(models.Enrollment.student_id == student_id).all()
