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
- **Authentication**: JWT
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

## Getting Started

1. Clone the repository:
```commandline
git clone https://github.com/yourusername/studysmart-ai-backend.git
cd studysmart-ai-backend
```
2. Set up a virtual environment:
```commandline
python -m venv venv
source venv/bin/activate # On Windows use venv\Scripts\activate
```
3. Install dependencies:
```commandline
pip install -r requirements.txt
```
4. Set up your environment variables:
```commandline
cp .env.example .env
```
5. Run the application:
```commandline
uvicorn app.main:app --reload
```
6. Visit `http://localhost:8000/docs` to see the Swagger UI documentation.

## Development

- Follow PEP 8 style guide for Python code.
- Write unit tests for new features.
- Update requirements.txt when adding new dependencies.

## API Documentation

Once the server is running, you can access the full API documentation at:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Contributing

We welcome contributions! Please see our [CONTRIBUTING.md](CONTRIBUTING.md) file for details on how to get started.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
