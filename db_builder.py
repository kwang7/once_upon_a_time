import sqlite3

DATABASE = "once_upon_a_time.db"

def create_tables():
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS stories (id INTEGER PRIMARY KEY, name TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS edits (story_id INTEGER, user_id INTEGER, timestamp INTEGER, content TEXT)")

    db.commit()
    db.close()
