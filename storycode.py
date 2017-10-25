import sqlite3
import db_builder
import datetime #used for timestamp

db_builder.create_tables()
DATABASE = db_builder.DATABASE

def add_story(story_id, story_name):
    db = sqlite3.connect(db_builder)
    c = db.cursor()
    cmd = "INSERT INTO stories(id, name) VALUES ("  + str(story_id) +  ", '" + story_name + "'" + ")"
    c.execute(cmd)
    db.commit()
    db.close()
#add_story(1, "One day...")
#add_story(2, "Anotha day...")

def see_table(table):
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    cmd = "SELECT * FROM " + table
    ret = c.execute(cmd)
    for thing in ret:
        print thing
    db.close()

see_table("stories")
print("\n")
def add_edit(story_id, user_id, timestamp, content):
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    formatted_time = timestamp.strftime("%Y-%m-%d %H:%M:%S")
    cmd = "INSERT INTO edits VALUES (" + str(story_id) + "," + str(user_id) + ", '" + \
            formatted_time + "', '" + content + "')"
    c.execute(cmd)
    db.commit()
    db.close()

def get_story(story_id):
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    query = "SELECT * FROM edits WHERE story_id =" + str(story_id) + " ORDER BY timestamp ASC"
    result = c.execute(query)
    for row in result:
        print row

#add_story(1,"Title")
add_edit(1,1,datetime.datetime.today(),"Edit 1")
add_edit(1,2,datetime.datetime.today(),"Edit 2")
add_edit(1,3,datetime.datetime.today(),"Edit 3")
get_story(1)
