from pydantic import BaseModel
from typing import List

class SubjectProgress(BaseModel):
    course_name: str
    student_progress: float
    average_progress: float
    median_progress: float

class StudentDashboardResponse(BaseModel):
    subjects_progress: List[SubjectProgress]
