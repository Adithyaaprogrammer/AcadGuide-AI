from sqlalchemy.orm import Session
import app.models.models as models

def create_assignment(db: Session, week_id: int, title: str, type: str):
    db_assignment = models.Assignment(week_id=week_id, title=title, type=type)
    db.add(db_assignment)
    db.commit()
    db.refresh(db_assignment)
    return db_assignment

def get_assignment(db: Session, assessment_id: int):
    return db.query(models.Assignment).filter(models.Assignment.id == assessment_id).first()

def get_week_assignments(db: Session, week_id: int):
    return db.query(models.Assignment).filter(models.Assignment.week_id == week_id).all()
