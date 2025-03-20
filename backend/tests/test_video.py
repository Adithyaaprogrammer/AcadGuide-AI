import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Suppress specific warnings
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning, module="sqlalchemy.*")  # SQLAlchemy deprecation
warnings.filterwarnings("ignore", category=DeprecationWarning, module="pydantic.*")    # Pydantic deprecation

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db, Base
from app.models.models import Video
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

# Use a separate test database
TEST_DATABASE_URL = "sqlite:///test.db"
TestEngine = create_engine(TEST_DATABASE_URL)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=TestEngine)

def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="function")
def test_client():
    Base.metadata.create_all(bind=TestEngine)
    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
    TestEngine.dispose()
    Base.metadata.drop_all(bind=TestEngine)
    if os.path.exists("test.db"):
        for _ in range(3):
            try:
                os.remove("test.db")
                break
            except PermissionError:
                import time
                time.sleep(0.5)
        else:
            print("Warning: Could not remove test.db after multiple attempts")

@pytest.fixture(scope="function")
def db_session(test_client):
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.rollback()
        db.close()

def test_create_video(test_client):
    # API being tested: POST /api/videos/
    #     Inputs: week_id=1, title="Intro Video", youtube_url="https://youtube.com/watch?v=123" (passed as query parameters)
    #     Expected output: 200 status code, {"week_id": 1, "title": "Intro Video", "youtube_url": "https://youtube.com/watch?v=123", "id": <generated_id>}
    #     Actual Output: Response status code and JSON body
    #     Result: Success
    response = test_client.post("/api/videos/", params={"week_id": 1, "title": "Intro Video", "youtube_url": "https://youtube.com/watch?v=123"})
    print(f"Create video response: {response.json()}")
    assert response.status_code == 200  # Consider 201 for creation in a RESTful API
    response_json = response.json()
    assert response_json["week_id"] == 1
    assert response_json["title"] == "Intro Video"
    assert response_json["youtube_url"] == "https://youtube.com/watch?v=123"
    assert "id" in response_json

def test_get_video(test_client, db_session: Session):
    # API being tested: GET /api/videos/1
    #     Inputs: Video with id=1, week_id=1, title="Sample Video", youtube_url="https://youtube.com/watch?v=456" pre-inserted into database
    #     Expected output: 200 status code, {"id": 1, "week_id": 1, "title": "Sample Video", "youtube_url": "https://youtube.com/watch?v=456"}
    #     Actual Output: Response status code and JSON body
    #     Result: Success
    video = Video(id=1, week_id=1, title="Sample Video", youtube_url="https://youtube.com/watch?v=456")
    db_session.add(video)
    db_session.commit()
    response = test_client.get("/api/videos/1")
    print(f"Get video response: {response.json()}")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "week_id": 1, "title": "Sample Video", "youtube_url": "https://youtube.com/watch?v=456"}