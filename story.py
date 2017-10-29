import sqlite3
import db_builder
import datetime #used for timestamp

DATABASE = db_builder.DATABASE

def new_story(title):
    '''
    Determines story_id and calls helper function to add it to the table
    Does not allow story titles that already exist
    '''

    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    check = "SELECT * FROM stories WHERE title='" + title + "'"
#    print "-------------- PRINTING CHECK --------------"
#    print check
    exists = c.execute(check).fetchall() #checking to see if this story exists already...
    # print "-------------- EXISTS for " + title + "--------------"
    # print (exists)
    if exists == []:
        query = "SELECT MAX(id) FROM stories"
        max_story_id = c.execute(query).fetchone()[0]
        if max_story_id == None:
            story_id = 1
        else:
            story_id = max_story_id + 1
        return add_story(story_id, str(title)) 
    else: 
        return "select another title"

    # print "STORY_ID....." + str(story_id)

def add_story(id, title):
    '''
    add story to the table
    '''
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    query = "INSERT INTO stories VALUES ('" + str(id) + "', '" + title + "')"
#    print "----------PRINTING QUERY -------"
#    print query
    c.execute(query)
    db.commit()
    db.close()

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
    cmd = "INSERT INTO edits VALUES (" + str(story_id) + "," + str(user_id) + ", '" + \
            formatted_time + "', '" + content + "')"
    c.execute(cmd)
    db.commit()
    db.close()

def get_story(story_id):
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    query = "SELECT * FROM edits WHERE story_id =" + str(story_id) + " ORDER BY timestamp ASC"
    story = c.execute(query)
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
    query = "SELECT content FROM edits WHERE timestamp = (SELECT MAX(timestamp) FROM edits WHERE story_id = " + str(story_id) + ")"
    result = c.execute(query)
    return result.fetchone()[0]


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

#------------------------------- HARDCODED STORY TITLES
if __name__ == "__main__":
    new_story("The Story of Once Upon A Time")
    new_story("Badum")
    new_story("8 Million Stories")

    '''
    print ("-----------ADDING STORIES------------------")
    new_story("The Story of Once Upon A Time") 
    new_story("Badum")
    new_story("8 Million Stories")
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
