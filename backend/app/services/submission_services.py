from sqlalchemy.orm import Session
import app.models.models as models

def create_submission(db: Session, assignment_id: int, student_id: int, content: str):
    db_submission = models.Submission(assignment_id=assignment_id, student_id=student_id, content=content, grade=None)
    db.add(db_submission)
    db.commit()
    db.refresh(db_submission)
    return db_submission

def grade_submission(db: Session, submission_id: int, grade: int):
    submission = db.query(models.Submission).filter(models.Submission.id == submission_id).first()
    if submission:
        submission.grade = grade
        db.commit()
        db.refresh(submission)
    return submission

def get_student_submissions(db: Session, student_id: int, assignment_id: int):
    return db.query(models.Submission).filter(
        models.Submission.student_id == student_id,
        models.Submission.assignment_id == assignment_id
    ).all()
