import story
import sqlite3
import db_builder

DATABASE = db_builder.DATABASE

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
    

print edited(1, 3)
