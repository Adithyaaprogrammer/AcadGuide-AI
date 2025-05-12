from sqlalchemy.orm import Session
import app.models.models as models
import app.schemas.schema as schemas

def get_course(db: Session, course_id: int):
    return db.query(models.Course).filter(models.Course.id == course_id).first()

def get_courses(db: Session):
    return db.query(models.Course).all()

def create_course(db: Session, course: schemas.CourseCreate):
    db_course = models.Course(title=course.title, instructor_id=course.instructor_id)
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

def get_instructor_courses(db: Session, instructor_id: int):
    return db.query(models.Course).filter(models.Course.instructor_id == instructor_id).all()
