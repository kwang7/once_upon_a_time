import sqlite3
import db_builder



db_builder.create_tables()

def add_story(story_id, story_name):
    db = sqlite3.connect(db_builder.DATABASE)
    c = db.cursor()
    cmd = "INSERT INTO stories(id, name) VALUES ("  + str(story_id) +  ", '" + story_name + "'" + ")"
    c.execute(cmd)
    db.commit()
    db.close()
    


#add_story(1, "One day...")
#add_story(2, "Anotha day...")

    
def see_table(table):
    db = sqlite3.connect(db_builder.DATABASE)
    c = db.cursor()
    cmd = "SELECT * FROM " + table
    ret = c.execute(cmd)
    for thing in ret:
        print thing
    db.close()
    
see_table("stories")
