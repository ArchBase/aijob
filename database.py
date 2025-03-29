import sqlite3

conn = sqlite3.connect("jobs.db")
c = conn.cursor()

c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT, resume TEXT, preferences TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS recruiters (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS jobs (id INTEGER PRIMARY KEY, recruiter_id INTEGER, title TEXT, description TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS applications (id INTEGER PRIMARY KEY, user_id INTEGER, job_id INTEGER, status TEXT, match_score REAL)")

# Add 'title' column if not exists
try:
    c.execute("ALTER TABLE jobs ADD COLUMN title TEXT")
except sqlite3.OperationalError:
    pass  # Column already exists

conn.commit()
conn.close()
