import sqlite3

conn = sqlite3.connect("jobs.db")
c = conn.cursor()

# Add 'description' column if not exists
c.execute("ALTER TABLE users ADD COLUMN description TEXT")
# Add 'match_score' column if not exists
c.execute("ALTER TABLE applications ADD COLUMN match_score REAL")

conn.commit()
conn.close()
