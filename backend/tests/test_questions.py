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
from app.models.models import Question, QuestionOption, CorrectOption
from app.schemas.schema import QuestionCreate, QuestionOptionCreate, CorrectOptionCreate
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

def test_create_question(test_client):
    # API being tested: POST /api/questions/
    #     Inputs: {"question_text": "What is 2+2?", "question_type": "multiple_choice", "assessment_id": 1, "week_id": null, "options": [{"option_text": "4"}, {"option_text": "5"}], "correct_option": {"option_id": 1}}
    #     Expected output: 200 status code, {"id": <generated_id>, "question_text": "What is 2+2?", "question_type": "multiple_choice", "assessment_id": 1, "week_id": null, "options": [{"id": <generated_id>, "option_text": "4"}, {"id": <generated_id>, "option_text": "5"}], "correct_option": {"id": <generated_id>, "option_id": <first_option_id>}}
    #     Actual Output: Response status code and JSON body
    #     Result: Success
    question_data = {
        "question_text": "What is 2+2?",
        "question_type": "multiple_choice",
        "assessment_id": 1,
        "week_id": None,
        "options": [
            {"option_text": "4"},
            {"option_text": "5"}
        ],
        "correct_option": {"option_id": 1}  # Note: This will be adjusted post-creation
    }
    response = test_client.post("/api/questions/", json=question_data)
    print(f"Create question response: {response.json()}")
    assert response.status_code == 200  # Router uses 200 by default; consider 201 for creation
    response_json = response.json()
    assert response_json["question_text"] == "What is 2+2?"
    assert response_json["question_type"] == "multiple_choice"
    assert response_json["assessment_id"] == 1
    assert response_json["week_id"] is None
    assert len(response_json["options"]) == 2
    assert response_json["options"][0]["option_text"] == "4"
    assert response_json["options"][1]["option_text"] == "5"
    assert "id" in response_json
    assert "correct_option" in response_json
    assert response_json["correct_option"]["option_id"] == response_json["options"][0]["id"]

def test_get_questions(test_client, db_session: Session):
    # API being tested: GET /api/questions/
    #     Inputs: Pre-inserted question with id=1, question_text="What is Python?", question_type="multiple_choice", assessment_id=1, options=["Yes", "No"], correct_option=first option
    #     Expected output: 200 status code, [{"id": 1, "question_text": "What is Python?", "question_type": "multiple_choice", "assessment_id": 1, "week_id": null, "options": [{"id": 1, "option_text": "Yes"}, {"id": 2, "option_text": "No"}], "correct_option": {"id": 1, "option_id": 1}}]
    #     Actual Output: Response status code and JSON body
    #     Result: Success
    db_question = Question(id=1, question_text="What is Python?", question_type="multiple_choice", assessment_id=1)
    db_session.add(db_question)
    db_session.commit()
    db_session.refresh(db_question)

    option1 = QuestionOption(id=1, question_id=db_question.id, option_text="Yes")
    option2 = QuestionOption(id=2, question_id=db_question.id, option_text="No")
    db_session.add_all([option1, option2])
    db_session.commit()

    correct_option = CorrectOption(id=1, question_id=db_question.id, option_id=option1.id)
    db_session.add(correct_option)
    db_session.commit()

    response = test_client.get("/api/questions/")
    print(f"Get questions response: {response.json()}")
    assert response.status_code == 200
    assert len(response.json()) == 1
    response_json = response.json()[0]
    assert response_json["id"] == 1
    assert response_json["question_text"] == "What is Python?"
    assert response_json["question_type"] == "multiple_choice"
    assert response_json["assessment_id"] == 1
    assert response_json["week_id"] is None
    assert len(response_json["options"]) == 2
    assert response_json["options"][0]["option_text"] == "Yes"
    assert response_json["options"][1]["option_text"] == "No"
    assert response_json["correct_option"]["option_id"] == response_json["options"][0]["id"]