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
from app.models.user_model import User
from app.schemas.user_schema import UserCreate
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from passlib.context import CryptContext
from fastapi.security import HTTPBasicCredentials
import base64

# Use a separate test database
TEST_DATABASE_URL = "sqlite:///test.db"
TestEngine = create_engine(TEST_DATABASE_URL)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=TestEngine)

# Password hashing context (same as in service)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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

def test_get_user(test_client, db_session: Session):
    # API being tested: GET /api/users/1
    #     Inputs: User with id=1, username="testuser", email="test@example.com", role="student", hashed_password pre-inserted into database
    #     Expected output: 200 status code, {"id": 1, "username": "testuser", "email": "test@example.com", "role": "student"}
    #     Actual Output: Response status code and JSON body
    #     Result: Success
    hashed_password = pwd_context.hash("password123")
    user = User(id=1, username="testuser", email="test@example.com", role="student", hashed_password=hashed_password)
    db_session.add(user)
    db_session.commit()
    response = test_client.get("/api/users/1")
    print(f"Get user response: {response.json()}")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "username": "testuser", "email": "test@example.com", "role": "student"}

def test_get_user_by_email(test_client, db_session: Session):
    # API being tested: GET /api/users/email/test@example.com
    #     Inputs: User with username="testuser", email="test@example.com", role="student", hashed_password pre-inserted into database
    #     Expected output: 200 status code, {"id": <generated_id>, "username": "testuser", "email": "test@example.com", "role": "student"}
    #     Actual Output: Response status code and JSON body
    #     Result: Success
    hashed_password = pwd_context.hash("password123")
    user = User(username="testuser", email="test@example.com", role="student", hashed_password=hashed_password)
    db_session.add(user)
    db_session.commit()
    response = test_client.get("/api/users/email/test@example.com")
    print(f"Get user by email response: {response.json()}")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["username"] == "testuser"
    assert response_json["email"] == "test@example.com"
    assert response_json["role"] == "student"
    assert "id" in response_json

def test_register_user(test_client):
    # API being tested: POST /api/users/
    #     Inputs: {"username": "newuser", "email": "newuser@example.com", "password": "newpass123", "role": "student"}
    #     Expected output: 201 status code, {"id": <generated_id>, "username": "newuser", "email": "newuser@example.com", "role": "student"}
    #     Actual Output: Response status code and JSON body
    #     Result: Success
    user_data = {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "newpass123",
        "role": "student"
    }
    response = test_client.post("/api/users/", json=user_data)
    print(f"Register user response: {response.json()}")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["username"] == "newuser"
    assert response_json["email"] == "newuser@example.com"
    assert response_json["role"] == "student"
    assert "id" in response_json

def test_authenticate_user(test_client, db_session: Session):
    # API being tested: POST /api/users/authenticate
    #     Inputs: HTTP Basic Auth with username="authuser", password="authpass123", user pre-inserted with hashed password
    #     Expected output: 200 status code, {"id": <generated_id>, "username": "authuser", "email": "auth@example.com", "role": "student"}
    #     Actual Output: assert 401 == 200
    #     Result: Failed
    hashed_password = pwd_context.hash("authpass123")
    user = User(username="authuser", email="auth@example.com", role="student", hashed_password=hashed_password)
    db_session.add(user)
    db_session.commit()
    # Create Basic Auth header
    credentials = base64.b64encode(b"authuser:authpass123").decode("ascii")
    headers = {"Authorization": f"Basic {credentials}"}
    response = test_client.post("/api/users/authenticate", headers=headers)
    print(f"Authenticate user response: {response.json()}")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["username"] == "authuser"
    assert response_json["email"] == "auth@example.com"
    assert response_json["role"] == "student"
    assert "id" in response_json