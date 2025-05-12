from fastapi import APIRouter, HTTPException
from typing import List
import app.services.smart_ai_services as smart_ai_service
from app.services.RAG_Model1 import get_course_recommendations
from app.services.resource_recommendation import get_resource_recommendations
from app.services.study_plan_service import get_study_plan
from pydantic import BaseModel
from fastapi import FastAPI
from app.routers import smart_ai_router
from fastapi.testclient import TestClient
# Initialize FastAPI TestClient
client = TestClient(app)

# --- Test Cases ---

# 1. Test `/ai/answer_question`
def test_answer_question():
    #Input: {"question": "What is machine learning}
    #Expected Output:Content and relavent resources without the actual answer
    #Actual Output: {"question": "What is machine learning", "answer": "The answer to your question is available in the lectures resources of the course machine learning techniques and machine learning practice . Please refer to the course content for more information."} 
    #Result: Pass
    response = client.post("/ai/answer_question", json={"question": "What is machine learning?"})
    assert response.status_code == 200
    assert "question" in response.json()
    assert "answer" in response.json()

def test_answer_question_empty():
    #Input: {"question": ""}
    #Expected Output: Error message "Question cannot be empty."
    #Actual Output: {"detail": "Question cannot be empty."}
    #Result: Pass
    response = client.post("/ai/answer_question", json={"question": ""})
    assert response.status_code == 400
    assert response.json()["detail"] == "Question cannot be empty."


# 2. Test `/ai/generate_study_plan`
def test_generate_study_plan():
    #Input: {"course_id": 101, "student_id": 1}
    #Expected Output: Study plan for the student for the course
    #Actual Output: {"student_id": 1, "course_id": 101, "study_plan": "reating a structured study plan for the Machine Learning Practice course at IIT Madras will help you effectively navigate the curriculum and maximize your learning outcomes. Below is a suggested 12-week study plan, aligning with the typical course structure:
# Week 1: Introduction to Machine Learning

# Understand the definition and scope of machine learning.
# Explore various applications and real-world use cases.
# Familiarize yourself with different types of machine learning: supervised, unsupervised, and reinforcement learning.
# Week 2: Calculus Refresher

# Review fundamental concepts of calculus relevant to machine learning, such as differentiation and integration.
# Understand how these concepts apply to optimization problems in machine learning.
# Week 3: Linear Algebra – Least Squares Regression

# Study vector spaces, matrices, and linear transformations.
# Learn about the least squares method for regression analysis.
# Week 4: Linear Algebra – Eigenvalues and Eigenvectors

# Understand the significance of eigenvalues and eigenvectors in data transformations.
# Explore their applications in dimensionality reduction techniques like Principal Component Analysis (PCA).
# Week 5: Linear Algebra – Symmetric Matrices

# Delve into the properties of symmetric matrices.
# Learn about their role in various machine learning algorithms.
# Week 6: Singular Value Decomposition (SVD) and PCA in Image Processing

# Study the concepts of SVD and its applications.
# Understand how PCA is used for dimensionality reduction and image compression.
# Week 7: Unconstrained Optimization

# Learn about optimization techniques without constraints.
# Explore gradient descent methods and their applications in training machine learning models.
# Week 8: Convex Sets, Functions, and Optimization Problems

# Understand the properties of convex sets and functions.
# Study their importance in formulating and solving optimization problems in machine learning.
# Week 9: Constrained Optimization and Lagrange Multipliers

# Explore techniques for solving optimization problems with constraints.
# Understand the application of Lagrange multipliers in such scenarios.
# Apply these concepts to logistic regression models.
# Week 10: Probabilistic Models in Machine Learning

# Study examples of probabilistic models used in machine learning tasks.
# Understand how probability theory underpins various algorithms.
# Week 11: Exponential Family of Distributions

# Learn about the exponential family of probability distributions.
# Explore their relevance in modeling and inference within machine learning.
# Week 12: Parameter Estimation and Expectation Maximization

# Understand methods for estimating parameters in statistical models.
# Study the Expectation-Maximization (EM) algorithm and its applications."}
    #Result: Pass
    response = client.post("/ai/generate_study_plan", json={"course_id": 101, "student_id": 1})
    assert response.status_code == 200
    assert "student_id" in response.json()
    assert "course_id" in response.json()
    assert "study_plan" in response.json()

def test_generate_study_plan_invalid_course():
    #Input: {"course_id": 999, "student_id": 1}
    #Expected Output: Error message "Invalid course ID"
    #Actual Output: {"error": "Invalid course ID"}
    #Result: Pass   
    response = client.post("/ai/generate_study_plan", json={"course_id": 999, "student_id": 1})
    assert response.status_code == 200
    assert "error" in response.json()
    assert response.json()["error"] == "Invalid course ID"


# 3. Test `/ai/structured_learning_path`
def test_structured_learning_path():
    #Input: {"level": "Diploma in Programming", "completed_courses": ["Database Management Systems", "Programming Data Structures & Algorithms using Python"]}
    #Expected Output: Learning path for the student based on the completed courses
    #Actual Output: {"level": "Diploma in Programming", "completed_courses": ["Database Management Systems", "Programming Data Structures & Algorithms using Python"], "learning_path": "Based on the information provided, I would recommend the following path for upcoming courses if you have already completed the Diploma in Programming with a focus on Database Management Systems, Programming Data Structures & Algorithms using Python, and other relevant courses:

# 1. Core 1 - Operating Systems & Computer Architecture
# 2. Core 2 - Software Testing & Software Engineering
# 3. Machine Learning Foundations
# 4. Machine Learning Technique
# 5. Machine Learning Practice
# 6. Business Data Management
# 7. Business Analytics
# 8. Tools in Data Science
# 9. Core 3 - AI: Search Methods for Problem Solving & Deep Learning
# 10. Design Thinking
# 11. Speech Technology
# 12. Deep Learning in Practice
# 13. Thematic Ideas in Data Science
# 14. Special topics in Machine Learning
# 15. Computer Vision

# This path starts with foundational computer science courses, moves into data management, business analytics, and machine learning, and then builds on those skills with more advanced topics in artificial intelligence and computer vision. The recommended order takes into account the prerequisites and natural progression of the topics.
     # Result: Pass
    data = {"level": "Diploma in Programming", "completed_courses": ["Python"]}
    response = client.post("/ai/structured_learning_path", json=data)
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


# 4. Test `/ai/resource_recommendation`
def test_resource_recommendation():
    #Input: {"topic": "Machine Learning"}
    #Expected Output: Recommended resources for the topic
    #Actual Output: {"topic": "Machine Learning", "Recommended Resources": "1. Machine Learning Foundations - IIT Madras Online Course 
    # 2. Machine Learning Techniques - IIT Madras Online Course
    # 3. Machine Learning Practice - IIT Madras Online Course
    # 4. Pattern Recognition and Machine Learning - Christopher M. Bishop
    # 5. Machine Learning Yearning - Andrew Ng"}
    # Result: Pass 
    data = {"topic": "Machine Learning"}
    response = client.post("/ai/resource_recommendation", json=data)
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert "Recommended Resources" in response.json()


# 5. Test `/assignment_reminders`
def test_assignment_reminders():
    #Input: {"student_id": 1, "assignment": "Complete Python Basics"}
    #Expected Output: Reminder sent
    #Actual Output: {"status": "Reminder sent"}
    #Result: Pass
    data = {"student_id": 1, "assignment": "Complete Python Basics"}
    response = client.post("/assignment_reminders", json=data)
    assert response.status_code == 200
    assert "status" in response.json()
    assert response.json()["status"] == "Reminder sent"


# 6. Test `/engagement_notifications`
def test_engagement_notifications():
    #Input: {"student_id": 1}
    #Expected Output: Engagement notification sent
    #Actual Output: {"notification": "Engagement notification sent"}
    #Result: Pass
    data = {"student_id": 1}
    response = client.post("/engagement_notifications", json=data)
    assert response.status_code == 200
    assert "notification" in response.json()
    assert response.json()["notification"] == "Engagement notification sent"


# 7. Test `/ai/debugging_tips`
def test_debugging_tips():
    #Input: {"code": "print('Hello World')"}
    #Expected Output: Debugging tips for the code
    #Actual Output: {"code": "print('Hello World')", "tips": "1. Check for syntax errors in the code.
# 2. Verify that the necessary libraries are imported.
# 3. Ensure that the code is correctly indented.
# 4. Use print statements to trace the flow of the program.
# 5. Check for typos in variable names or function calls."}
    #Result: Pass
    data = {"code": "print('Hello World')"}
    response = client.post("/ai/debugging_tips", json=data)
    assert response.status_code == 200
    assert "tips" in response.json()


# 8. Test `/ai/common_errors_faqs`
def test_common_errors_faqs():
    #Input: None
    #Expected Output: FAQs for common errors
    #Actual Output: {"FAQs": "1. How do I resolve a syntax error in Python?
# 2. What should I do if my code is stuck in an infinite loop?
# 3. How can I fix the 'ModuleNotFoundError' in my Python code?
# 4. Why am I getting a 'NameError' in my code?
# 5. How do I troubleshoot a 'TypeError' in Python?"}
    #Result : Pass
    response = client.get("/ai/common_errors_faqs")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert "FAQs" in response.json()


# 9. Test `/ai/portal_assistance`
def test_portal_assistance():
    #Input: {"issue": "Unable to log in"}
    #Expected Output: Solution for the issue
    #Actual Output: {"issue": "Unable to log in", "solution": "If you are unable to log in to the portal, please follow these steps:
# 1. Check your username and password for typos.
# 2. Ensure that the CAPS LOCK key is turned off.
# 3. Reset your password using the 'Forgot Password' option.
# 4. Contact the system administrator for further assistance."}
    #Result : Pass
    data = {"issue": "Unable to log in"}
    response = client.post("/ai/portal_assistance", json=data)
    assert response.status_code == 200
    assert "solution" in response.json()
