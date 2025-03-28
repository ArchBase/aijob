import sqlite3

conn = sqlite3.connect("jobs.db")
c = conn.cursor()



conn.commit()
conn.close()
