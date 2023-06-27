from flask import render_template, url_for
from app import app
from models import *


@app.route('/')
def main_page():
    # print(url_for("main_page"))
    return render_template("main_page.html", title="Главная страница")


@app.route('/profile/')
def profile_page():
    return render_template("profile.html", title="Профиль", name="name")


@app.route('/reviews/')
def reviews_page():
    return render_template("reviews.html", title="Отзывы")


@app.route('/review/<int:id>/')
def review(id):
    return f"Отзыв ID: {id}"
    # return render_template("main_page.html", title="Profile")
