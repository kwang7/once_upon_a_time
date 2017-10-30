import db_builder
import sqlite3
import datetime #used for timestamp

DATABASE = "once_upon_a_time.db"

def add_story(title):
    '''
    Adds story to the stories table in the database
    '''
    added = False
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    check = "SELECT * FROM stories WHERE title= ?"
    exists = c.execute(check,(title,)).fetchall() #checking to see if this story exists already...
    # fetchall() returns an empty list if teh story doesn't exist
    if exists == []:
        query = "INSERT INTO stories VALUES (NULL,?)"
        c.execute(query,(title,))
        num = c.lastrowid
        added = True
    db.commit()
    db.close()
    # If the story was added, return the new story's id otherwise False
    # Kind of bad programming
    if added:
        return num
    return False

# Quick testing code to see the values in a table
def see_table(table):
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    cmd = "SELECT * FROM " + table
    ret = c.execute(cmd)
    for thing in ret:
        print(thing)
    db.close()

def add_edit(story_id, user_id, content):
    '''
    Add an edit to a story given a story and user id, and the edit contents
    '''
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    # Using the datetime module, convert the given time to the format:
    # YYYY-mm-dd HH:MM:SS
    # e.g. 1970-01-01 00:00:00
    formatted_time = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    cmd = "INSERT INTO edits VALUES (?,?,?,?)"
    c.execute(cmd, (str(story_id), str(user_id), formatted_time, content))
    db.commit()
    db.close()

def get_story(story_id):
    '''
    Given a story, return all of its edits
    '''
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    query = "SELECT content FROM edits WHERE story_id = ? ORDER BY timestamp ASC"
    story = c.execute(query, (str(story_id),))
    story = story.fetchall()
    db.close()
    return story
    return result.fetchone()[0]

def latest_story_edit(story_id):
    '''
    Returns the content of the latest update for a specific story
    '''
    try:
        last = get_story(story_id)[-1]
        return last[0]
    except:
        return ""


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
    print("-----------PRINTING LATEST EDIT OF STORY_ID = 1 ---------------")
    print latest_story_edit(1)

    """

    print("-----------SEE_TABLE('STORIES') ---------------")
    see_table("stories")
    print("\n")
