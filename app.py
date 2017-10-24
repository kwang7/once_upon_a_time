from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session

app = Flask(__name__)

@app.route("/", methods=['GET','POST'])
def index():
    return "Hi!"

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
