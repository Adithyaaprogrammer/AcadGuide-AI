from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import app.services.video_services as video_service
from ..database import get_db

router = APIRouter()

@router.post("/videos/")
def create_video(week_id: int, title: str, youtube_url: str, db: Session = Depends(get_db)):
    return video_service.create_video(db, week_id, title, youtube_url)

@router.get("/videos/{video_id}")
def get_video(video_id: int, db: Session = Depends(get_db)):
    return video_service.get_video(db, video_id)
