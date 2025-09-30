import os
from flask import Flask, render_template, request, redirect, url_for
from bus_system import ZoteeStation

template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'bus-ji', 'templates'))
app = Flask(__name__, template_folder=template_dir)
station = ZoteeStation()

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/home")
def home():
    return render_template("home.html")

if __name__ == '__main__':
    app.run(debug=True)