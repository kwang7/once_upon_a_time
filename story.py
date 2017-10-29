import sqlite3
import db_builder
import datetime #used for timestamp

DATABASE = db_builder.DATABASE

def add_story(title):
    '''
    add story to the table
    '''
    added = False
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    check = "SELECT * FROM stories WHERE title= ?"
    exists = c.execute(check,(title,)).fetchall() #checking to see if this story exists already...
    if exists == []:
        query = "INSERT INTO stories VALUES (NULL,?)"
        c.execute(query,(title,))
        added = True
    db.commit()
    db.close()
    return added

def see_table(table):
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    cmd = "SELECT * FROM " + table
    ret = c.execute(cmd)
    for thing in ret:
        print(thing)
    db.close()

def add_edit(story_id, user_id, content):
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    formatted_time = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    cmd = "INSERT INTO edits VALUES (?,?,?,?)"
    c.execute(cmd, (str(story_id), str(user_id), formatted_time, content))
    db.commit()
    db.close()

def get_story(story_id):
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    query = "SELECT * FROM edits WHERE story_id = ? ORDER BY timestamp ASC"
    story = c.execute(query, (str(story_id),))
    db.close()
    if story:
        return story
    return []

# add_story(1,"Title")
# add_edit(1,1,datetime.datetime.today(),"Edit 1")
# add_edit(1,2,datetime.datetime.today(),"Edit 2")
# add_edit(1,3,datetime.datetime.today(),"Edit 3")
# for row in get_story(1):
#     print row

def get_last_edit():
    '''
    Last update in the table
    '''
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    query = "SELECT content FROM edits WHERE timestamp = (SELECT MAX(timestamp) FROM edits)"
    result = c.execute(query)
    return result.fetchone()[0]

def latest_story_edit(story_id):
    '''
    Returns the content of the latest update for a specific story
    '''
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    query = "SELECT content FROM edits WHERE timestamp = (SELECT MAX(timestamp) FROM edits WHERE story_id = ? )"
    result = c.execute(query, (story_id,))
    try:
        return result.fetchone()[0]
    except TypeError:
        return ""

def titles():
    '''
    Returns story titles
    '''
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    query = "SELECT title, id FROM stories"
    result = c.execute(query).fetchall()
    titles = []
    for t in result:
        titles.append(t)
    return titles

def get_title(story_id):
    '''
    Given story's id, returns story's title
    '''
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    query = "SELECT title FROM stories WHERE id = ?"
    title = c.execute(query,(story_id,)).fetchone()[0]
    return title

#------------------------------- HARDCODED STORY TITLES
if __name__ == "__main__":
    add_story("The Story of Once Upon A Time")
    add_story("Badum")
    add_story("8 Million Stories")

    print (get_title(1))
    print (get_title(2))


    '''
    print ("-----------ADDING STORIES------------------")
    add_story("The Story of Once Upon A Time")
    add_story("Badum")
    add_story("8 Million Stories")
    see_table("stories")


    print ("-----------PRINTING TITLES------------------")
    print titles()
    '''
    """
    add_edit(1,1, "Edit 1")
    add_edit(1,2, "Edit 2")
    add_edit(1,3, "Edit 3")

    get_story(1)
    print("-----------PRINTING LATEST EDIT ---------------")
    get_last_edit()

    print("-----------PRINTING LATEST EDIT OF STORY_ID = 1 ---------------")
    print latest_story_edit(1)

    """

    print("-----------SEE_TABLE('STORIES') ---------------")
    see_table("stories")
    print("\n")
