from flask import render_template, url_for
from app import app
from models import *


@app.route('/')
def main_page():
    print(url_for("main_page"))
    return render_template("main_page.html", title="Main")


@app.route('/posts/<int:id>')
def posts(id):
    return f"Пользователь: {id}"
    # return render_template("main_page.html", title="Profile")
