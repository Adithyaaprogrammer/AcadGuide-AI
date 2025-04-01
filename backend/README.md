# StudySmart AI Backend

Welcome to the StudySmart AI backend repository! This project serves as the core of our Learning Management System (LMS), providing a robust and scalable solution for modern education needs.

## Features

- **User Management**: Separate interfaces for students and instructors
- **Course Management**: Support for up to 4 enrolled courses per student
- **Content Organization**: 4 weeks of course material per course
- **Rich Media Support**: 4-5 embedded YouTube videos per week
- **Assignment Types**: Weekly graded, practice, and coding assignments
- **Progress Tracking**: Detailed student progress monitoring
- **AI-Powered Learning**: Utilizes cutting-edge AI for personalized learning experiences

## Tech Stack

- **Framework**: FastAPI
- **Language**: Python 3.9+
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Authentication**: Cookie-based sessions
- **API Documentation**: Swagger UI (auto-generated)

## Project Structure

```
backend/
├── app/
│ ├── main.py
│ ├── models/
│ │ ├── init.py
│ │ ├── user.py
│ │ ├── course.py
│ │ └── assignment.py
│ ├── routers/
│ │ ├── init.py
│ │ ├── student.py
│ │ └── instructor.py
│ ├── schemas/
│ │ ├── init.py
│ │ ├── user.py
│ │ ├── course.py
│ │ └── assignment.py
│ └── database.py
├── requirements.txt
└── README.md
```

## API Documentation

Once the server is running, you can access the full API documentation at:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`


