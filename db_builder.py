import sqlite3
import story
import user

DATABASE = "once_upon_a_time.db"

def create_tables():
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS stories (id INTEGER PRIMARY KEY, title TEXT NOT NULL)")
    c.execute("CREATE TABLE IF NOT EXISTS edits (story_id INTEGER NOT NULL, user_id INTEGER NOT NULL, timestamp INTEGER NOT NULL, content TEXT NOT NULL)")
    c.execute("CREATE TABLE IF NOT EXISTS users ( username TEXT , password TEXT, id INTEGER PRIMARY KEY )")

    db.commit()
    db.close()

# Generate stories, users, and edits to ease testing
def seed_db():
    # ADD USERS
    user.add_user("test_user", "test_pass")
    user.add_user("cool_person", "cool_pass")
    user.add_user("mr_brown", "brown mykolyk")
    user.add_user("mr_dw", "dyrland weaver")

    # ADD SOME STORIES
    s1 = story.add_story("Three Little Pigs")
    story.add_edit(s1, 1, "Once upon a time there was an old mother pig who had three little pigs and not enough food to feed them. So when they were old enough, she sent them out into the world to seek their fortunes.")
    story.add_edit(s1, 2, "The first little pig was very lazy. He didn't want to work at all and he built his house out of straw.")
    story.add_edit(s1, 3, "The second little pig worked a little bit harder but he was somewhat lazy too and he built his house out of sticks." )

    s2 = story.add_story("I'm a 911 Operator")
    story.add_edit(s2, 2, '''CREDITS TO r/nosleep
    "911, what is your emergency?"

    "Yeah, hi, um...This is going to sound kind of strange but there's a man stumbling around in circles in my front yard."

    "...could you repeat that, sir?"

    "He looks...sick, or lost, or drunk, or something. I just woke up to get a glass of water and heard snow crunching around underneath my front window so I peeked out...I'm looking at him now, he's about ten yards away from my window. Something's not right."

    "What is your address, sir?"

    "1617 Quarry Lane, in Pinella Pass."

    "I'm going to send a squad car your way, but that's quite a ways out. Are you alone in your house sir?"

    "Yes, I'm alone."''')
    story.add_edit(s2,3,'''
"Can you confirm that all of your doors and windows are locked? Stay on the phone with me."

"I know that my front is definitely locked, but I'll go check my back door again really quick.

...

I appreciate your help, by the way, I know this is kind of strange but I really hope that -"

...

"...Sir? Are you still there?"

"He's...he's still in the yard yard. But he's...what the f***...he's upside down..."

"Sir? Stay on with me, what is happening?"

"He's staring right at me...but he's...he's standing on his hands now. He's perfectly still, staring straight at me. He's doing a handstand and he's smiling at me and not moving."

"He's...he's doing a handstand, sir?"
    ''')
    story.add_edit(s2,4,'''
        "I...I don't know how he...yeah, he's facing me and standing on his hands and he's got this huge smile and he's perfectly still...what the F***...please get someone out here NOW."

        "Sir I need you to remain calm. I've put out the call and an officer is on his way."

        "His teeth are so huge...what the f***, please help me..."

        "Sir I want you to try and keep an eye on him but make sure your back door is locked again. We need to make sure all possible access points are secured. Can you talk me through and confirm that your back door is locked?"

        "Okay...I'm walking backwards now and keeping him in my sight...

        My hand is on the back doorknob now...it's locked. I need to check the deadbolt so I'm going to take my eyes off of him for a split second."

        "Alright sir. Help is on the way. Just stay on the phone with me, everything's going to be alright.

        Sir?

        ...

        ...Sir? Are you still there?"

        "He's...his face. It's up against the glass."
        ''')
