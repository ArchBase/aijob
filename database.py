import sqlite3

conn = sqlite3.connect("jobs.db")
c = conn.cursor()

c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT, resume TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS recruiters (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS jobs (id INTEGER PRIMARY KEY, recruiter_id INTEGER, description TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS applications (id INTEGER PRIMARY KEY, user_id INTEGER, job_id INTEGER, status TEXT)")

# Add 'description' column if not exists
c.execute("ALTER TABLE users ADD COLUMN preferences TEXT")
# Add 'match_score' column if not exists
c.execute("ALTER TABLE applications ADD COLUMN match_score REAL")

conn.commit()
conn.close()
