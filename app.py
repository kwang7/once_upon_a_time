from flask import Flask, render_template, request, session, redirect, url_for, flash
import os

app = Flask(__name__)


@app.route("/", methods=['GET','POST'])
def index():
    #if username is in session, redirect to homepage
    if "username" in session:
        return "hi"
    #login or sign up options
    return render_template("howdy.html")

@app.route('/auth', methods = ["GET", "POST"])
def auth():
    return "auth"

@app.route('/signup', methods = ["GET", "POST"])
def signup():
    if "username" not in session:    
        return render_template("signup.html")
    if request.args["password"] != request.args["password2"]:
        flash('Passwords dont match')
        return render_template("signup.html")
    else:
        return redirect(url_for("auth"))
   

    
@app.route('/login', methods = ["GET", "POST"])
def login():
    if "username" in session:
        return redirect(url_for("auth"))
    return render_template("login.html")

@app.route('/welcome', methods = ["GET", "POST"])
def welcome():
    if "username" in session:
        return render_template("home.html", username = username)
    return redirect(url_for("auth"))

@app.route('/view', methods=['GET', 'POST'])
def view():
    return "This is a deep story."

@app.route('/create', methods=['GET', 'POST'])
def create():
    return "Here you would create a story..."

@app.route('/stories', methods=['GET', 'POST'])
def stories():
    return "There's a list of unedited stories somewhere..."

@app.route('/edit', methods=['GET','POST'])
def edit():
    return "Wow you're editing a story!"

if __name__ == "__main__":
    app.debug = True
    app.run()
