from fastapi import FastAPI, Depends, Request, status, HTTPException, Response
from app.routes import auth, instructor_routes
from app.routes import (
    user_routes, course_routes, enrollment_routes, 
    week_routes, assignment_routes, video_routes, 
    submission_routes, smart_ai_routes,question_routes, student_routes
)
from app.database import engine, Base
from app import models
from starlette.middleware.sessions import SessionMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI(title="StudySmart AI")
app.add_middleware(SessionMiddleware, secret_key="your-secret-key")
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])

app.include_router(user_routes.router, prefix="/api", tags=["Users"])
app.include_router(course_routes.router, prefix="/api", tags=["Courses"])
app.include_router(enrollment_routes.router, prefix="/api", tags=["Enrollments"])
app.include_router(week_routes.router, prefix="/api", tags=["Weeks"])
app.include_router(assignment_routes.router, prefix="/api", tags=["Assignments"])
app.include_router(video_routes.router, prefix="/api", tags=["Videos"])
app.include_router(submission_routes.router, prefix="/api", tags=["Submissions"])
app.include_router(smart_ai_routes.router, prefix="/api", tags=["AI Services"])
app.include_router(question_routes.router, prefix="/api", tags=["Questions"])
app.include_router(student_routes.router, prefix="/student", tags=["Student"])
app.include_router(instructor_routes.router, prefix="/instructor", tags=["Instructor"])



@app.get("/protected")
def protected_route(request: Request):
    username = request.cookies.get('session')
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    return {"message": f"Hello, {username}! This is a protected route."}
# app.include_router(student.router, prefix="/student", tags=["Student"], dependencies=[Depends(get_current_user)])
# app.include_router(instructor.router, prefix="/instructor", tags=["Instructor"], dependencies=[Depends(get_current_user)])

@app.get("/")
def read_root():
    return {"message": "Welcome to StudySmart AI LMS"}
