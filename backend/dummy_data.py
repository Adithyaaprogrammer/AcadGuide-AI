import sqlite3
from app.services.user_services import get_password_hash as hash_password

# Connect to SQLite database
conn = sqlite3.connect('users.db')
cursor = conn.cursor()
print("Connected to SQLite database 'users.db'")

# Drop existing tables
tables = ['users', 'courses', 'weeks', 'videos', 'enrollments', 'assessments', 'questions', 'question_options', 'correct_options', 'submissions']
for table in tables:
    cursor.execute(f'DROP TABLE IF EXISTS {table}')
    print(f"Dropped table if it existed: {table}")

# Create tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    hashed_password TEXT NOT NULL,
    role TEXT NOT NULL
)
''')
print("Created table: users")

cursor.execute('''
CREATE TABLE IF NOT EXISTS courses (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    instructor_id INTEGER,
    FOREIGN KEY (instructor_id) REFERENCES users (id)
)
''')
print("Created table: courses")

cursor.execute('''
CREATE TABLE IF NOT EXISTS weeks (
    id INTEGER PRIMARY KEY,
    course_id INTEGER,
    week_number INTEGER NOT NULL,
    FOREIGN KEY (course_id) REFERENCES courses (id)
)
''')
print("Created table: weeks")

cursor.execute('''
CREATE TABLE IF NOT EXISTS videos (
    id INTEGER PRIMARY KEY,
    week_id INTEGER,
    title TEXT NOT NULL,
    youtube_url TEXT NOT NULL,
    FOREIGN KEY (week_id) REFERENCES weeks (id)
)
''')
print("Created table: videos")

cursor.execute('''
CREATE TABLE IF NOT EXISTS enrollments (
    id INTEGER PRIMARY KEY,
    student_id INTEGER,
    course_id INTEGER,
    FOREIGN KEY (student_id) REFERENCES users (id),
    FOREIGN KEY (course_id) REFERENCES courses (id)
)
''')
print("Created table: enrollments")

cursor.execute('''
CREATE TABLE IF NOT EXISTS assessments (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL
)
''')
print("Created table: assessments")

cursor.execute('''
CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY,
    assessment_id INTEGER,
    week_id INTEGER,
    question_text TEXT NOT NULL,
    question_type TEXT NOT NULL,
    FOREIGN KEY (assessment_id) REFERENCES assessments (id),
    FOREIGN KEY (week_id) REFERENCES weeks (id)
)
''')
print("Created table: questions")

cursor.execute('''
CREATE TABLE IF NOT EXISTS question_options (
    id INTEGER PRIMARY KEY,
    question_id INTEGER,
    option_text TEXT NOT NULL,
    FOREIGN KEY (question_id) REFERENCES questions (id)
)
''')
print("Created table: question_options")

cursor.execute('''
CREATE TABLE IF NOT EXISTS correct_options (
    id INTEGER PRIMARY KEY,
    question_id INTEGER UNIQUE,
    option_id INTEGER,
    FOREIGN KEY (question_id) REFERENCES questions (id),
    FOREIGN KEY (option_id) REFERENCES question_options (id)
)
''')
print("Created table: correct_options")

cursor.execute('''
CREATE TABLE IF NOT EXISTS submissions (
    id INTEGER PRIMARY KEY,
    assessment_id INTEGER,
    student_id INTEGER,
    content TEXT NOT NULL,
    grade INTEGER,
    FOREIGN KEY (assessment_id) REFERENCES assessments (id),
    FOREIGN KEY (student_id) REFERENCES users (id)
)
''')
print("Created table: submissions")

# Insert sample data with hashed passwords
users = [
            ("VKP", "vkp@example.com", hash_password("password1"), "student"),
    ("AK", "ak@example.com", hash_password("password2"), "student"),
    ("PS", "ps@example.com", hash_password("password3"), "instructor")
]
cursor.executemany('INSERT INTO users (username, email, hashed_password, role) VALUES (?, ?, ?, ?)', users)
print("Inserted sample data into table: users")

courses = [
    ("DSA", 3),
    ("SC", 3),
    ("Python", 3),
    ("Java", 3)
]
cursor.executemany('INSERT INTO courses (title, instructor_id) VALUES (?, ?)', courses)
print("Inserted sample data into table: courses")

weeks = [
    (1, 1), (1, 2), (1, 3), (1, 4),
    (2, 1), (2, 2), (2, 3), (2, 4),
    (3, 1), (3, 2), (3, 3), (3, 4),
    (4, 1), (4, 2), (4, 3), (4, 4)
]
cursor.executemany('INSERT INTO weeks (course_id, week_number) VALUES (?, ?)', weeks)
print("Inserted sample data into table: weeks")

videos = [
    (1, "Video 1", "http://youtube.com/1"),
    (2, "Video 2", "http://youtube.com/2"),
    (3, "Video 3", "http://youtube.com/3"),
    (4, "Video 4", "http://youtube.com/4")
]
cursor.executemany('INSERT INTO videos (week_id, title, youtube_url) VALUES (?, ?, ?)', videos)
print("Inserted sample data into table: videos")

enrollments = [
    (1, 1), (1, 2), (1, 3), (1, 4),
    (2, 1), (2, 2), (2, 3), (2, 4)
]
cursor.executemany('INSERT INTO enrollments (student_id, course_id) VALUES (?, ?)', enrollments)
print("Inserted sample data into table: enrollments")

assessments = [
    ("Assessment 1",),
    ("Assessment 2",)
]
cursor.executemany('INSERT INTO assessments (title) VALUES (?)', assessments)
print("Inserted sample data into table: assessments")

questions = [
    (1, None, "Question 1", "MCQ"),
    (2, None, "Question 2", "Short Answer")
]
cursor.executemany('INSERT INTO questions (assessment_id, week_id, question_text, question_type) VALUES (?, ?, ?, ?)', questions)
print("Inserted sample data into table: questions")

question_options = [
    (1, "Option 1"),
    (1, "Option 2")
]
cursor.executemany('INSERT INTO question_options (question_id, option_text) VALUES (?, ?)', question_options)
print("Inserted sample data into table: question_options")

correct_options = [
    (1, 1)
]
cursor.executemany('INSERT INTO correct_options (question_id, option_id) VALUES (?, ?)', correct_options)
print("Inserted sample data into table: correct_options")

submissions = [
    (1, 1, "Content 1", 85),
    (2, 2, "Content 2", 90)
]
cursor.executemany('INSERT INTO submissions (assessment_id, student_id, content, grade) VALUES (?, ?, ?, ?)', submissions)
print("Inserted sample data into table: submissions")

# Commit and close
conn.commit()
conn.close()
print("Committed changes and closed the connection")