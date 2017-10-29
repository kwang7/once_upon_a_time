import story
import sqlite3
import db_builder

DATABASE = db_builder.DATABASE

def add_user(username, password):
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    query = 'SELECT id FROM users WHERE username= ?'
    existing_user = c.execute(query, (username,))
    added = False
    if not existing_user.fetchone():
        c.execute("INSERT INTO users VALUES (?,?,NULL)", (username,password))
        added = True
    db.commit()
    db.close()
    return added

def auth_user(username, password):
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    query = 'SELECT password FROM users WHERE username = ? AND password = ?'
    user = c.execute(query,(username,password))
    if user:
        return True
    return False

def get_user_id(username):
    '''
    Gets user id from use with username = username
    '''
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    query = 'SELECT id FROM users WHERE username="' + username + '"'
    result = c.execute(query)
    if result:
        return result.fetchone()
    else:
        return -1

def get_stories(user_id):
    '''
    Returns a list of stories edited by user id = user_id
    '''
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    query = "SELECT DISTINCT stories.id, title FROM stories, edits \
            WHERE edits.story_id = stories.id AND edits.user_id=" + str(user_id)
    stories = c.execute(query)
    return stories.fetch()
    db.close()

def edited(story_id, user_id):
    '''
    Returns true if the user edited the story with story id = story_id
    '''
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    query = "SELECT story_id FROM edits WHERE user_id = " + str(user_id) + " AND story_id = " + str(story_id)
    result = c.execute(query)
    if result:
        return True
    else:
        return False

def all_unedited(user_id):
    '''
    Returns a list of all unedited story ids
    '''
    query = "SELECT Count(*) FROM stories"
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    number = c.execute(query).fetchone()[0]
    unedited_ids = []
    for i in range(1, number + 1):
        if not edited(i, user_id):
            unedited_ids.append(i)
    return unedited_ids

if __name__ == "__main__":
    print all_unedited(1)
    print edited(1, 3)
