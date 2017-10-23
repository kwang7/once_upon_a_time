from flask import Flask, render_template
app = Flask(__name__)

@app.route("/", methods=['GET','POST'])
def index():
    return "Hi!"

if __name__ == "__main__":
    app.debug = True
    app.run()
