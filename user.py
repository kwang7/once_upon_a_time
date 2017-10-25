import storycode
import sqlite3
import db_builder

DATABASE = db_builder.DATABASE

def get_stories(user_id):
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    query = "SELECT DISTINCT stories.id, title FROM stories, edits \
            WHERE edits.story_id = stories.id AND edits.user_id=" + str(user_id)
    stories = c.execute(query)
    for story in stories:
        print story
    db.close()
