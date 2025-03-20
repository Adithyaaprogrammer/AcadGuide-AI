import sqlite3
import enum

# Define UserType enum
class UserType(enum.Enum):
    student = "student"
    instructor = "instructor"

# Database setup
DB_FILE = "users.db"

# Create users table if it doesn't exist
def create_table():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        user_type TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

# Insert a user into the database
def insert_user(name, email, user_type):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO users (name, email, user_type) VALUES (?, ?, ?)
    ''', (name, email, user_type.value))
    conn.commit()
    conn.close()

# Sample user data
users_data = [
    {"name": "John Doe", "email": "john@example.com", "user_type": UserType.student},
    {"name": "Jane Smith", "email": "jane@example.com", "user_type": UserType.student},
    {"name": "Prof. Alice Johnson", "email": "alice@university.edu", "user_type": UserType.instructor},
    {"name": "Bob Brown", "email": "bob@example.com", "user_type": UserType.student},
    {"name": "Dr. Carol White", "email": "carol@university.edu", "user_type": UserType.instructor},
    {"name": "David Lee", "email": "david@example.com", "user_type": UserType.student},
    {"name": "Prof. Eve Taylor", "email": "eve@university.edu", "user_type": UserType.instructor},
]

# Create table and insert users
def main():
    create_table()
    for user in users_data:
        try:
            insert_user(user["name"], user["email"], user["user_type"])
            print(f"Added user: {user['name']}")
        except sqlite3.IntegrityError:
            print(f"User with email {user['email']} already exists. Skipping.")

if __name__ == "__main__":
    main()
    print("User data creation complete.")
