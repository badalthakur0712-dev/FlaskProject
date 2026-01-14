import sqlite3

conn = sqlite3.connect("college.db")
cursor = conn.cursor()

# Create chatbot table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS chatbot (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    answer TEXT NOT NULL
)
""")

# Create users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
""")

# Add default admin user (replace username/password if you want)
cursor.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", 
               ("admin", "admin123"))

conn.commit()
conn.close()

print("Database & users table created successfully!")
