import sqlite3

DATABASE = "once_upon_a_time.db"

def create_tables():
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS stories (id INTEGER PRIMARY KEY, title TEXT NOT NULL)")
    c.execute("CREATE TABLE IF NOT EXISTS edits (story_id INTEGER NOT NULL, user_id INTEGER NOT NULL, timestamp INTEGER NOT NULL, content TEXT NOT NULL)")
    c.execute("CREATE TABLE IF NOT EXISTS users ( username TEXT , password TEXT, id INTEGER PRIMARY KEY )")

    db.commit()
    db.close()
