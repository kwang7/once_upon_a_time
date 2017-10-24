import sqlite3
import db_builder



db_builder.create_tables()

def add_story(story_id, story_name):
    db = sqlite3.connect(db_builder.DATABASE)
    c = db.cursor()
    cmd = "INSERT INTO stories(id, name) VALUES ("  + str(story_id) +  ", '" + story_name + "'" + ")"
    print cmd


add_story(1, "One day...")
    
