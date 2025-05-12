from fastapi import APIRouter, HTTPException
from typing import List
import app.services.smart_ai_services as smart_ai_service
from app.services.RAG_Model1 import get_course_recommendations
from app.services.resource_recommendation import get_resource_recommendations
from app.services.study_plan_service import get_study_plan
from pydantic import BaseModel

# Pydantic model for structured learning path request
class LearningPathRequest(BaseModel):
    level: str
    completed_courses: List[str]

# Pydantic model for study plan request
class StudyPlanRequest(BaseModel):
    course_id: int
    student_id: int

# Pydantic model for resource recommendation
class ResourceRequest(BaseModel):
    topic: str

# Pydantic model for assignment reminders
class AssignmentReminderRequest(BaseModel):
    student_id: int
    assignment: str

# Pydantic model for engagement notifications
class EngagementNotificationRequest(BaseModel):
    student_id: int

# Pydantic model for debugging tips
class DebuggingTipsRequest(BaseModel):
    code: str

# Pydantic model for portal assistance
class PortalAssistanceRequest(BaseModel):
    issue: str

# Pydantic model for student progress
class StudentProgressRequest(BaseModel):
    student_id: int


# Initialize API Router
router = APIRouter()


# --- AI Assistance for Students ---

@router.post("/ai/answer_question")
def answer_question(question: str):
    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")
    return smart_ai_service.answer_question(question)


@router.post("/ai/generate_study_plan")
def generate_study_plan(request: StudyPlanRequest):
    try:
        study_plan = get_study_plan(request.course_id, request.student_id)
        return study_plan
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating study plan: {str(e)}")


@router.post("/ai/structured_learning_path")
def structured_learning_path(request: LearningPathRequest):
    try:
        return get_course_recommendations(request.level, request.completed_courses)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating learning path: {str(e)}")


@router.post("/ai/resource_recommendation")
def resource_recommendation(request: ResourceRequest):
    try:
        return get_resource_recommendations(request.topic)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving resources: {str(e)}")


@router.post("/assignment_reminders")
def assignment_reminders(request: AssignmentReminderRequest):
    try:
        return smart_ai_service.assignment_reminders(request.student_id, request.assignment)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sending assignment reminder: {str(e)}")


@router.post("/engagement_notifications")
def engagement_notifications(request: EngagementNotificationRequest):
    try:
        return smart_ai_service.engagement_notifications(request.student_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sending engagement notification: {str(e)}")


@router.post("/ai/debugging_tips")
def debugging_tips(request: DebuggingTipsRequest):
    try:
        return smart_ai_service.debugging_tips(request.code)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error providing debugging tips: {str(e)}")


# --- Instructor Stories ---

@router.get("/ai/common_errors_faqs")
def common_errors_faqs():
    try:
        return smart_ai_service.common_errors_faqs()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching FAQs: {str(e)}")


# --- Support Staff & Parent Stories ---

@router.post("/ai/portal_assistance")
def portal_assistance(request: PortalAssistanceRequest):
    try:
        return smart_ai_service.portal_assistance(request.issue)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error providing portal assistance: {str(e)}")

