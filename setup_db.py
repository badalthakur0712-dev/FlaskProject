import sqlite3

# Connect to database (it will create if not exists)
conn = sqlite3.connect("college.db")
cursor = conn.cursor()

# Create users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
""")

# Create chatbot table
cursor.execute("""
CREATE TABLE IF NOT EXISTS chatbot (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT,
    answer TEXT
)
""")

# Insert default admin user
try:
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("admin", "admin123"))
except:
    pass  # ignore if already exists

conn.commit()
conn.close()

print("Database and tables created successfully!")
