import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_user():
    """
    API being tested: POST /api/users
    Inputs: {"username": "user1", "email": "user1@example.com", "role": "student", "password": "password1"}
    Expected output: 201 status code, {"username": "user1"}
    Actual Output: Response status code and JSON body
    Result: Success/Fail
    """
    response = client.post("/api/users", json={"username": "user1", "email": "user1@example.com", "role": "student", "password": "password1"})
    assert response.status_code == 201
    assert response.json()["username"] == "user1"

def test_create_course():
    """
    API being tested: POST /api/courses
    Inputs: {"title": "Course 1", "instructor_id": 1}
    Expected output: 201 status code, {"title": "Course 1"}
    Actual Output: Response status code and JSON body
    Result: Success/Fail
    """
    response = client.post("/api/courses", json={"title": "Course 1", "instructor_id": 1})
    assert response.status_code == 201
    assert response.json()["title"] == "Course 1"

def test_create_enrollment():
    """
    API being tested: POST /api/enrollments
    Inputs: {"student_id": 1, "course_id": 1}
    Expected output: 201 status code, {"student_id": 1}
    Actual Output: Response status code and JSON body
    Result: Success/Fail
    """
    response = client.post("/api/enrollments", json={"student_id": 1, "course_id": 1})
    assert response.status_code == 201
    assert response.json()["student_id"] == 1

def test_login():
    """
    API being tested: POST /auth/login
    Inputs: {"username": "user1", "password": "password1"}
    Expected output: 200 status code, {"access_token": ...}
    Actual Output: Response status code and JSON body
    Result: Success/Fail
    """
    response = client.post("/auth/login", json={"username": "user1", "password": "password1"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_get_users():
    """
    API being tested: GET /api/users
    Inputs: None
    Expected output: 200 status code, list of users
    Actual Output: Response status code and JSON body
    Result: Success/Fail
    """
    response = client.get("/api/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_courses():
    """
    API being tested: GET /api/courses
    Inputs: None
    Expected output: 200 status code, list of courses
    Actual Output: Response status code and JSON body
    Result: Success/Fail
    """
    response = client.get("/api/courses")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_enrollments():
    """
    API being tested: GET /api/enrollments
    Inputs: None
    Expected output: 200 status code, list of enrollments
    Actual Output: Response status code and JSON body
    Result: Success/Fail
    """
    response = client.get("/api/enrollments")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_student_dashboard():
    """
    API being tested: GET /student/student_dashboard
    Inputs: None
    Expected output: 200 status code, {"subjects_progress": ...}
    Actual Output: Response status code and JSON body
    Result: Success/Fail
    """
    response = client.get("/student/student_dashboard")
    assert response.status_code == 200
    assert "subjects_progress" in response.json()

def test_instructor_dashboard():
    """
    API being tested: GET /instructor/instructor_dashboard
    Inputs: None
    Expected output: 200 status code, {"courses_progress": ...}
    Actual Output: Response status code and JSON body
    Result: Success/Fail
    """
    response = client.get("/instructor/instructor_dashboard")
    assert response.status_code == 200
    assert "courses_progress" in response.json()