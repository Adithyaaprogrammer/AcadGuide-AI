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
from app.schemas.schema import CourseCreate
from app.models.models import Course
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

def test_get_course(test_client, db_session: Session):
    # API being tested: GET /api/courses/1
    #     Inputs: Course with id=1, title="Test Course", instructor_id=1 pre-inserted into database
    #     Expected output: 200 status code, {"id": 1, "title": "Test Course", "instructor_id": 1}
    #     Actual Output: Response status code and JSON body
    #     Result: Success
    course = Course(id=1, title="Test Course", instructor_id=1)
    db_session.add(course)
    db_session.commit()
    response = test_client.get("/api/courses/1")
    print(f"Get course response: {response.json()}")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "title": "Test Course", "instructor_id": 1}

def test_get_courses(test_client, db_session: Session):
    # API being tested: GET /api/courses/
    #     Inputs: Two courses pre-inserted into database (id=1, title="Test Course 1", instructor_id=1) and (id=2, title="Test Course 2", instructor_id=2)
    #     Expected output: 200 status code, [{"id": 1, "title": "Test Course I", "instructor_id": 1}, {"id": 2, "title": "Test Course 2", "instructor_id": 2}]
    #     Actual Output: Response status code and JSON body
    #     Result: Success
    course1 = Course(id=1, title="Test Course 1", instructor_id=1)
    course2 = Course(id=2, title="Test Course 2", instructor_id=2)
    db_session.add_all([course1, course2])
    db_session.commit()
    response = test_client.get("/api/courses/")
    print(f"Get courses response: {response.json()}")
    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "title": "Test Course 1", "instructor_id": 1},
        {"id": 2, "title": "Test Course 2", "instructor_id": 2}
    ]

def test_create_course(test_client):
    # API being tested: POST /api/courses/
    #     Inputs: {"title": "New Course", "instructor_id": 1}
    #     Expected output: 200 status code, {"title": "New Course", "instructor_id": 1, "id": <generated_id>} (Note: 201 is more RESTful for creation)
    #     Actual Output: Response status code and JSON body
    #     Result: Success
    course_data = {"title": "New Course", "instructor_id": 1}
    response = test_client.post("/api/courses/", json=course_data)
    print(f"Create course response: {response.json()}")
    assert response.status_code == 200  
    response_json = response.json()
    assert response_json["title"] == "New Course"
    assert response_json["instructor_id"] == 1
    assert "id" in response_json

def test_get_instructor_courses(test_client, db_session: Session):
    # API being tested: GET /api/courses/instructor/1
    #     Inputs: Course with id=1, title="Course for Instructor 1", instructor_id=1 pre-inserted into database
    #     Expected output: 200 status code, [{"id": 1, "title": "Course for Instructor 1", "instructor_id": 1}]
    #     Actual Output: Response status code and JSON body
    #     Result: Success
    course = Course(id=1, title="Course for Instructor 1", instructor_id=1)
    db_session.add(course)
    db_session.commit()
    response = test_client.get("/api/courses/instructor/1")
    print(f"Get instructor courses response: {response.json()}")
    assert response.status_code == 200
    assert response.json() == [{"id": 1, "title": "Course for Instructor 1", "instructor_id": 1}]