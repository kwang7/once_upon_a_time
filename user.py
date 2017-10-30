import db_builder
import story
import sqlite3
import hashlib

DATABASE = "once_upon_a_time.db"

def add_user(username, password):
    '''
    Takes a username and password and adds it as a user
    Hashes the password using sha-256
    '''
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    query = 'SELECT id FROM users WHERE username= ?'
    existing_user = c.execute(query, (username,))
    added = False
    if not existing_user.fetchone():
        c.execute("INSERT INTO users VALUES (?,?,NULL)", \
                (username,hashlib.sha256(password).hexdigest()))
        added = True
    db.commit()
    db.close()
    return added

def auth_user(username, password):
    '''
    Checks if there is a user with the username and password specified
    '''
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    query = 'SELECT password FROM users WHERE username = ? AND password = ?'
    user = c.execute(query,(username,hashlib.sha256(password).hexdigest())).fetchone()
    if user:
        return True
    return False

def get_user_id(username):
    '''
    Gets user id corresponding to the given username
    '''
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    query = 'SELECT id FROM users WHERE username= ?'
    result = c.execute(query, (username,)).fetchone()
    if result:
        return result[0]
    else:
        return -1

def get_stories(user_id):
    '''
    Returns a list of stories the given user has edited
    '''
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    query = "SELECT DISTINCT stories.id, title FROM stories, edits \
            WHERE edits.story_id = stories.id AND edits.user_id = ?"
    stories = c.execute(query, (str(user_id),)).fetchall()
    db.close()
    return stories

def edited(story_id, user_id):
    '''
    Returns true if the user edited the story with the given id
    '''
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    query = "SELECT story_id FROM edits WHERE user_id = ? AND story_id = ?"
    result = c.execute(query, (str(user_id), str(story_id))).fetchone()
    return not (result is None)

def all_unedited(user_id):
    '''
    Returns a list of all stories not yet edited by the given user
    In the format of a list of lists, with the internal list [TITLE, ID]
    '''
    query = "SELECT Count(*) FROM stories"
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    number = c.execute(query).fetchone()[0]
    unedited_stories = []
    for i in range(1, number + 1):
        if not edited(i, user_id):
            unedited_stories.append([story.get_title(i), i])
    return unedited_stories

if __name__ == "__main__":
    print (all_unedited(1))
    print (edited(1, 3))
