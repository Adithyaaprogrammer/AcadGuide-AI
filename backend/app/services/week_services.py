from sqlalchemy.orm import Session
import app.models.models as models

def create_week(db: Session, course_id: int, week_number: int):
    db_week = models.Week(course_id=course_id, week_number=week_number)
    db.add(db_week)
    db.commit()
    db.refresh(db_week)
    return db_week

def get_week(db: Session, week_id: int):
    return db.query(models.Week).filter(models.Week.id == week_id).first()
