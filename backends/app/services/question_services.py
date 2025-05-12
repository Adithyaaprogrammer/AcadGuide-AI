from sqlalchemy.orm import Session
from app.models.models import Question, QuestionOption, CorrectOption
from app.schemas.schema import QuestionCreate

def create_question(db: Session, question: QuestionCreate):
    db_question = Question(
        question_text=question.question_text,
        question_type=question.question_type,
        assessment_id=question.assessment_id,
        week_id=question.week_id
    )

    db.add(db_question)
    db.commit()
    db.refresh(db_question)

    # Add options
    for option in question.options:
        db_option = QuestionOption(question_id=db_question.id, option_text=option.option_text)
        db.add(db_option)
        db.commit()
        db.refresh(db_option)

        # Check if this is the correct option
        if db_option.id == question.correct_option.option_id:
            db_correct_option = CorrectOption(question_id=db_question.id, option_id=db_option.id)
            db.add(db_correct_option)
            db.commit()

    return db_question

def get_questions(db: Session):
    return db.query(Question).all()
