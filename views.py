from flask import render_template, url_for, request, session, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from app import app
from models import *


@app.route('/')
def main_page():
    return render_template("main_page.html", title="Главная страница")


@app.route('/profile/')
@login_required
def profile_page():
    return render_template("profile.html", title="Профиль", name="name")


@app.route('/login/', methods=('POST', 'GET'))
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = db.session.execute(db.select(Users).filter_by(username=username)).scalar_one()
        if user and check_password_hash(user.password, password):
            session['logged_in'] = True
            login_user(user, remember=True)
            return redirect(request.args.get("next") or url_for('profile'))

    return render_template("login.html", title="Авторизация")


@app.route('/register/', methods=('POST', 'GET'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if len(username) > 4 and len(password) > 4:
            try:
                hashed_password = generate_password_hash(password)

                user = Users(username=username, password=hashed_password)
                db.session.add(user)
                db.session.commit()
            except:
                db.session.rollback()
        session['logged_in'] = True

        return redirect(url_for('profile'))

    return render_template("register.html", title="Регистрация")


@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))



@app.route('/reviews/')
@login_required
def reviews_page():
    return render_template("reviews.html", title="Отзывы")


@app.route('/review/<int:id>/')
@login_required
def review(id):
    return f"Отзыв ID: {id}"
    # return render_template("main_page.html", title="Profile")
