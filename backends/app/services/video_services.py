from sqlalchemy.orm import Session
import app.models.models as models

def create_video(db: Session, week_id: int, title: str, youtube_url: str):
    db_video = models.Video(week_id=week_id, title=title, youtube_url=youtube_url)
    db.add(db_video)
    db.commit()
    db.refresh(db_video)
    return db_video

def get_video(db: Session, video_id: int):
    return db.query(models.Video).filter(models.Video.id == video_id).first()
