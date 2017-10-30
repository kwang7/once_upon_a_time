from flask import Flask, render_template, request, session, redirect, url_for, flash
import sqlite3
import db_builder
import story
import user
import os

db_builder.create_tables()

app = Flask(__name__)
app.secret_key = os.urandom(32)

@app.route("/", methods=['GET','POST'])
def index():
    #if username is in session, redirect to homepage if "username" in session:
    if "username" in session:
        return redirect(url_for("welcome"))
    #login or sign up options
    return render_template("howdy.html")

@app.route('/signup', methods = ["GET", "POST"])
def signup():
    if "username" not in session:
        return render_template("signup.html")
    else:
        flash("Already logged in!")
        return redirect(url_for("welcome"))

@app.route('/signauth', methods = ["GET", "POST"])
def signauth():
    try:
        username = request.form['username']
        password = request.form['password']
        password2 = request.form['password2']
    except KeyError:
        flash("Please fill out all fields")
        return render_template("signup.html")
    if password != password2:
        flash("Passwords don't match")
        return render_template("signup.html")
    if username == "" or password == "" or password2 == "":
        flash("Fields must not be blank")
        return render_template("signup.html")
    if user.add_user(username, password):
        flash("Successfully created!")
        return redirect(url_for('login'))
    else:
        flash("Username taken")
        return redirect(url_for('signup'))

@app.route('/login', methods = ["GET", "POST"])
def login():
    if "username" in session:
        flash("Already logged in!")
        return redirect(url_for("welcome"))
    return render_template('login.html')

@app.route('/auth', methods = ["GET", "POST"])
def auth():
    #user already logged in
    if "username" in session:
        return redirect(url_for("welcome"))
    if request.method == "GET":
        #user went to /auth without logging in
        return redirect("/")
    try:
        username = request.form['username']
        password = request.form['password']
    except KeyError:
        flash("Please fill out all fields")
        return render_template("login.html")
    if user.auth_user(username,password):
        session['username'] = username
        flash("Successfully logged in")
        return redirect(url_for('welcome'))
    else:
        flash("Failed login")
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    if "username" not in session:
        flash("You aren't logged in")
        return redirect(url_for('login'))
    session.pop("username")
    flash("You've been logged out")
    return redirect(url_for('index'))

@app.route('/welcome', methods = ["GET", "POST"])
def welcome():
    if "username" in session:
        username = session["username"]
        return render_template("home.html", username = session["username"], \
                stories=user.get_stories(user.get_user_id(username)))
    return redirect(url_for("auth"))

@app.route('/view', methods=['GET', 'POST'])
def view():
    if "username" not in session:
        flash('You must be logged in to view stories!')
        return redirect(url_for('login'))
    story_id = request.args['story']
    #print story_id
    edited = user.edited(story_id, user.get_user_id(session['username']))
    if edited:
        content = story.get_story(story_id)
    else:
        content = story.latest_story_edit(story_id)
    return render_template('storypage.html', story_title=story.get_title(story_id), content=content, edited=edited, story=story_id)

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

        user_id = user.get_user_id(username)
        story.add_edit(story_id, user_id, content)
        flash("Story successfully created")
        return redirect(url_for('view', story=story_id))
    return render_template("create.html")

@app.route('/stories', methods=['GET', 'POST'])
def stories():
    if "username" not in session:
        flash('You must be logged in to view stories!')
        return redirect(url_for('login'))
    username = session["username"]
    return render_template('stories.html', stories=user.all_unedited(user.get_user_id(username)))

@app.route('/edit', methods=['GET','POST'])
def edit():
    if "username" not in session:
        flash('You must be logged in to edit!')
        return redirect(url_for('login'))
    story_id = request.args['story']
    user_id = user.get_user_id(session['username'])
    if user.edited(story_id, user_id):
        flash("You've already edited this story!")
        return redirect(url_for('welcome'))
    if request.method == "POST":
        try:
            content = request.form['content']
        except KeyError:
            flash('You have not filled out all the required fields')
            return redirect(url_for('edit'), story=story_id)
        story.add_edit(story_id, user_id, content)
        flash("Edited story")
        return redirect(url_for('welcome'))
    else:
        return render_template('edit.html',
                story_title=story.get_title(story_id),
                last_update=story.latest_story_edit(story_id),
                story=story_id)

# Passes this variable into every view
@app.context_processor
def logged_in():
    if "username" in session:
        return dict(logged_in=True)
    return dict(logged_in=False)

if __name__ == "__main__":
    app.debug = True
    app.run()
