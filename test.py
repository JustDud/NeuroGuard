import sqlite3

with sqlite3.connect("User_Data.db") as conn:
    cursor = conn.cursor()
    cursor.execute("ALTER TABLE data ADD COLUMN daily_goal_progression INTEGER")
    conn.commit()