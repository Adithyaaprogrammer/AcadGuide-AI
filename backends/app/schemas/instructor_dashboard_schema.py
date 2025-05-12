from pydantic import BaseModel
from typing import List, Dict

class CourseProgress(BaseModel):
    course_name: str
    average_progress: float
    median_progress: float
    student_progress_list: List[float]

class InstructorDashboardResponse(BaseModel):
    courses_progress: List[CourseProgress]