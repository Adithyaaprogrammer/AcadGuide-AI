from pydantic import BaseModel
from typing import List, Optional

class QuestionOptionBase(BaseModel):
    option_text: str

class QuestionOptionCreate(QuestionOptionBase):
    pass

class QuestionOptionResponse(QuestionOptionBase):
    id: int

    class Config:
        from_attributes = True

class CorrectOptionBase(BaseModel):
    option_id: int

class CorrectOptionCreate(CorrectOptionBase):
    pass

class CorrectOptionResponse(CorrectOptionBase):
    id: int

    class Config:
        from_attributes = True

class QuestionBase(BaseModel):
    question_text: str
    question_type: str
    assessment_id: Optional[int] = None
    week_id: Optional[int] = None

class QuestionCreate(QuestionBase):
    options: List[QuestionOptionCreate]
    correct_option: CorrectOptionCreate

class QuestionResponse(QuestionBase):
    id: int
    options: List[QuestionOptionResponse]
    correct_option: Optional[CorrectOptionResponse]

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: str

class CourseCreate(BaseModel):
    title: str
    instructor_id: int

class WeekCreate(BaseModel):
    course_id: int
    week_number: int

class AssignmentCreate(BaseModel):
    week_id: int
    title: str
    type: str

class VideoCreate(BaseModel):
    week_id: int
    title: str
    youtube_url: str

class EnrollmentCreate(BaseModel):
    student_id: int
    course_id: int

class SubmissionCreate(BaseModel):
    assessment_id: int
    student_id: int
    content: str
    grade: Optional[int] = None
