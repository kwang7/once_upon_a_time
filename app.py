from flask import Flask, render_template, request, session, redirect, url_for, flash
import sqlite3
import story
import user
import os

app = Flask(__name__)
app.secret_key = os.urandom(32)

f = "once_upon_a_time.db"
db = sqlite3.connect(f, check_same_thread=False)
c = db.cursor()

#------------------------------- HARDCODED STORY TITLES -------------------------------
story.new_story("The Story of Once Upon A Time")                                                                                       
story.new_story("Badum")                                                                                                              
story.new_story("8 Million Stories")  
#----------------------------------------------------------------------------------------

@app.route("/", methods=['GET','POST'])
def index():
    #if username is in session, redirect to homepage if "username" in session:
    if "username" in session:
        return redirect(url_for("auth"))
    #login or sign up options
    return render_template("howdy.html")

@app.route('/signup', methods = ["GET", "POST"])
def signup():
    if "username" not in session:
        return render_template("signup.html")
    else:
        return redirect(url_for("auth"))

@app.route('/signauth', methods = ["GET", "POST"])
def signauth():
    #print request.form
    if request.form["password"] != request.form["password2"]:
        flash("Passwords don't match")
        return render_template("signup.html")
    c.execute("INSERT INTO users VALUES (?,?)", (request.form["username"], request.form["password"]))
    session["username"] = request.form["username"]
    return redirect(url_for("auth"))

@app.route('/login', methods = ["GET", "POST"])
def login():
    if "username" in session:
        return redirect(url_for("auth"))
    return render_template("login.html")

@app.route('/auth', methods = ["GET", "POST"])
def auth():
    if "username" in session:
        return redirect(url_for("welcome"))
    else:

        # q = "SELECT password FROM userInfo WHERE username = \"" + session["username"] + "\" AND password = \"" + session["password"]
        # #WHERE username = " + session["username"]
        # foo = c.execute(q)
        # print(foo)
        flash("not authenticated")
        return redirect(url_for("index"))

@app.route('/welcome', methods = ["GET", "POST"])
def welcome(story_id):
    if "username" in session:
        return render_template("home.html", username = session["username"], story_titles=story.titles())
    return redirect(url_for("auth"))

@app.route('/view', methods=['GET', 'POST'])
def view(story_id):
    if "username" not in session:
        flash('You must be logged in to view stories!')
        return redirect(url_for('login'))
    # TODO - INCOMPLETE
    story_id = request.args['story']
    story.get_story(story_id)
    return "This is a deep story."

# TODO - TEST ONCE LOGIN SYSTEM IS UP & RUNNING
@app.route('/create', methods=['GET', 'POST'])
def create():
    if "username" not in session:
        flash('You must be logged in to create a story!')
        return redirect(url_for('login'))
    if request.method == "POST":
        try:
            title = request.form['title']
            content = request.form['content']
        except KeyError:
            flash('You have not filled out all the required fields')
            return redirect(url_for('create'))
        username = session['username']

        story_id = story.add_story(title)

        # What if the user_id returns -1
        user_id = user.get_user_id(username)
        story.add_edit(story_id, user_id, content)
        return redirect(url_for('view'), story=story_id)
    return "Here you would create a story..."

@app.route('/stories', methods=['GET', 'POST'])
def stories():
    if "username" not in session:
        flash('You must be logged in to view stories!')
        return redirect(url_for('login'))
    return "There's a list of unedited stories somewhere..."

@app.route('/edit', methods=['GET','POST'])
def edit():
    if "username" not in session:
        flash('You must be logged in to edit!')
        return redirect(url_for('login'))
    # TODO - Incomplete
    if request.method == "POST":
        try:
            story_id = request.form['story_id']
            content = request.form['content']
        except KeyError:
            flash('You have not filled out all the required fields')
            return redirect(url_for('edit'))
        # Logic for retrieving what story they are contributing to?
        # stories = user.get_stories(
        # storycode.add_edit(
    else:
        return redirect(url_for('index'))


@app.route('/story_content', methods=['GET', 'POST'])
def story_content():
    story_id = request.args.get('id', '')
    if "username" not in session:
        flash('You must be logged in to edit!')
        return redirect(url_for('login'))
    else: 
        db = sqlite3.connect(DATABASE)
        c = db.cursor()
        check = "SELECT * FROM edits, WHERE story_id='" + story_id + "' AND user_id = "+ get_user_id(session['username'])
        print check
        exists = c.execute(check).fetchall() #checking to see if this story exists already...     
        if exists != []:
            return redirect(url_for('view'), story_id = story_id)
        else:
            return redirect(url_for('edit'), story_id = story_id)


if __name__ == "__main__":
    app.debug = True
    app.run()

db.commit()
db.close()
