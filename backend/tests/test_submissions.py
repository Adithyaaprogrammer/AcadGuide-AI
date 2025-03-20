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
from app.models.models import Submission
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

def test_create_submission(test_client):
    # API being tested: POST /api/submissions/
    #     Inputs: assessment_id=1, student_id=1, content="This is my submission" (passed as query parameters)
    #     Expected output: 200 status code, {"assessment_id": 1, "student_id": 1, "content": "This is my submission", "grade": null, "id": <generated_id>}
    #     Actual Output: Response status code and JSON body
    #     Result: Success
    response = test_client.post("/api/submissions/", params={"assessment_id": 1, "student_id": 1, "content": "This is my submission"})
    print(f"Create submission response: {response.json()}")
    assert response.status_code == 200  # Consider 201 for creation in a RESTful API
    response_json = response.json()
    assert response_json["assessment_id"] == 1
    assert response_json["student_id"] == 1
    assert response_json["content"] == "This is my submission"
    assert response_json["grade"] is None
    assert "id" in response_json

def test_grade_submission(test_client, db_session: Session):
    # API being tested: POST /api/submissions/grade
    #     Inputs: submission_id=1, grade=85 (passed as query parameters), with a pre-inserted submission (id=1, assessment_id=1, student_id=1, content="Test submission", grade=None)
    #     Expected output: 200 status code, {"id": 1, "assessment_id": 1, "student_id": 1, "content": "Test submission", "grade": 85}
    #     Actual Output: Response status code and JSON body
    #     Result: Success
    submission = Submission(id=1, assessment_id=1, student_id=1, content="Test submission", grade=None)
    db_session.add(submission)
    db_session.commit()
    response = test_client.post("/api/submissions/grade", params={"submission_id": 1, "grade": 85})
    print(f"Grade submission response: {response.json()}")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["id"] == 1
    assert response_json["assessment_id"] == 1
    assert response_json["student_id"] == 1
    assert response_json["content"] == "Test submission"
    assert response_json["grade"] == 85

def test_get_student_submissions(test_client, db_session: Session):
    # API being tested: GET /api/submissions/student/1
    #     Inputs: Two submissions with student_id=1, assessment_id=1 pre-inserted into database (id=1, content="Submission 1", grade=None) and (id=2, content="Submission 2", grade=90)
    #     Expected output: 200 status code, [{"id": 1, "assessment_id": 1, "student_id": 1, "content": "Submission 1", "grade": null}, {"id": 2, "assessment_id": 1, "student_id": 1, "content": "Submission 2", "grade": 90}]
    #     Actual Output: Response status code and JSON body
    #     Result: Success
    submission1 = Submission(id=1, assessment_id=1, student_id=1, content="Submission 1", grade=None)
    submission2 = Submission(id=2, assessment_id=1, student_id=1, content="Submission 2", grade=90)
    db_session.add_all([submission1, submission2])
    db_session.commit()
    response = test_client.get("/api/submissions/student/1", params={"assessment_id": 1})
    print(f"Get student submissions response: {response.json()}")
    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "assessment_id": 1, "student_id": 1, "content": "Submission 1", "grade": None},
        {"id": 2, "assessment_id": 1, "student_id": 1, "content": "Submission 2", "grade": 90}
    ]