from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from ..database import Base

# class User(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String, unique=True, index=True)
#     email = Column(String, unique=True, index=True)
#     hashed_password = Column(String)
#     role = Column(String)

#     courses = relationship("Course", back_populates="instructor")
#     enrollments = relationship("Enrollment", back_populates="student")
#     submissions = relationship("Submission", back_populates="student")

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    instructor_id = Column(Integer, ForeignKey("users.id"))

    instructor = relationship("User", back_populates="courses")
    weeks = relationship("Week", back_populates="course")
    enrollments = relationship("Enrollment", back_populates="course")
    
class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)

    questions = relationship("Question", back_populates="assessment")
    submissions = relationship("Submission", back_populates="assessments")

class Week(Base):
    __tablename__ = "weeks"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"))
    week_number = Column(Integer, nullable=False)

    questions = relationship("Question", back_populates="week")
    videos = relationship("Video", back_populates="week")
    course = relationship("Course", back_populates="weeks") 

class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    week_id = Column(Integer, ForeignKey("weeks.id"))
    title = Column(String)
    youtube_url = Column(String)

    week = relationship("Week", back_populates="videos")

class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"))
    course_id = Column(Integer, ForeignKey("courses.id"))

    student = relationship("User", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")

class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)
    assessment_id = Column(Integer, ForeignKey("assessments.id"))
    student_id = Column(Integer, ForeignKey("users.id"))
    content = Column(Text)
    grade = Column(Integer, nullable=True)

    assessments = relationship("Assessment", back_populates="submissions")
    student = relationship("User", back_populates="submissions")

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    assessment_id = Column(Integer, ForeignKey("assessments.id"), nullable=True)
    week_id = Column(Integer, ForeignKey("weeks.id"), nullable=True)
    question_text = Column(Text, nullable=False)
    question_type = Column(String, nullable=False)  # e.g., 'MCQ', 'Short Answer', 'True/False'

    options = relationship("QuestionOption", back_populates="question", cascade="all, delete-orphan")
    correct_option = relationship("CorrectOption", back_populates="question", uselist=False)
    assessment = relationship("Assessment", back_populates="questions")
    week = relationship("Week", back_populates="questions")


class QuestionOption(Base):
    __tablename__ = "question_options"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"))
    option_text = Column(String, nullable=False)

    question = relationship("Question", back_populates="options")

class CorrectOption(Base):
    __tablename__ = "correct_options"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"), unique=True)
    option_id = Column(Integer, ForeignKey("question_options.id"))

    question = relationship("Question", back_populates="correct_option")
    option = relationship("QuestionOption")
