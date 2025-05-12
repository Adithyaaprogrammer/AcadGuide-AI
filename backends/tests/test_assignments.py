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
from app.models.models import Assessment
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

def test_create_Assessment(test_client):
    # API being tested: POST /api/Assessments/
    #     Inputs: week_id=1, title="Test Assessment", type="quiz" (passed as query parameters)
    #     Expected output: 200 status code, {"week_id": 1, "title": "Test Assessment", "type": "quiz", "id": <generated_id>}
    #     Actual Output: assert 404 == 200
    #     Result: failed
    response = test_client.post("/api/Assessments/", params={"week_id": 1, "title": "Test Assessment", "type": "quiz"})
    print(f"Create Assessment response: {response.json()}")
    assert response.status_code == 200  # Consider 201 for creation in a RESTful API
    response_json = response.json()
    assert response_json["week_id"] == 1
    assert response_json["title"] == "Test Assessment"
    assert response_json["type"] == "quiz"
    assert "id" in response_json

def test_get_Assessment(test_client, db_session: Session):
    # API being tested: GET /api/Assessments/1
    #     Inputs: Assessment with id=1, week_id=1, title="Sample Assessment", type="homework" pre-inserted into database
    #     Expected output: 200 status code, {"id": 1, "week_id": 1, "title": "Sample Assessment", "type": "homework"}
    #     Actual Output: UnboundLocalError: cannot access local variable 'Assessment' where it is not associated with a value
    #     Result: failed
    Assessment = Assessment(id=1, week_id=1, title="Sample Assessment", type="homework")
    db_session.add(Assessment)
    db_session.commit()
    response = test_client.get("/api/Assessments/1")
    print(f"Get Assessment response: {response.json()}")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "week_id": 1, "title": "Sample Assessment", "type": "homework"}

def test_get_week_Assessments(test_client, db_session: Session):
    # API being tested: GET /api/Assessments/week/1
    #     Inputs: Two Assessments with week_id=1 pre-inserted into database (id=1, title="Assessment 1", type="quiz") and (id=2, title="Assessment 2", type="essay")
    #     Expected output: 200 status code, [{"id": 1, "week_id": 1, "title": "Assessment 1", "type": "quiz"}, {"id": 2, "week_id": 1, "title": "Assessment 2", "type": "essay"}]
    #     Actual Output: TypeError: 'week_id' is an invalid keyword argument for Assessment
    #     Result: failed
    Assessment1 = Assessment(id=1, week_id=1, title="Assessment 1", type="quiz")
    Assessment2 = Assessment(id=2, week_id=1, title="Assessment 2", type="essay")
    db_session.add_all([Assessment1, Assessment2])
    db_session.commit()
    response = test_client.get("/api/Assessments/week/1")
    print(f"Get week Assessments response: {response.json()}")
    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "week_id": 1, "title": "Assessment 1", "type": "quiz"},
        {"id": 2, "week_id": 1, "title": "Assessment 2", "type": "essay"}
    ]