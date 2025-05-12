from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from app.services.question_services import create_question, get_questions
from app.schemas.schema import QuestionCreate, QuestionResponse

router = APIRouter()

@router.post("/questions/", response_model=QuestionResponse)
def create_question_endpoint(question: QuestionCreate, db: Session = Depends(get_db)):
    return create_question(db, question)

@router.get("/questions/", response_model=list[QuestionResponse])
def get_questions_endpoint(db: Session = Depends(get_db)):
    return get_questions(db)
