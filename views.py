from flask import render_template, url_for, request, session, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from app import app
from models import *
from forms import LoginForm, RegisterForm, CategoryForm, ReviewForm


@app.route('/')
def main_page():
    return render_template("main_page.html", title="Главная страница")


@app.route('/profile/')
@login_required
def profile_page():
    return render_template("profile.html", title="Профиль")


@app.route('/login/', methods=('POST', 'GET'))
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile_page'))

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        try:
            user = db.session.execute(db.select(Users).filter_by(username=username)).scalar_one()
            if user and check_password_hash(user.password, password):
                session['logged_in'] = True
                login_user(user, remember=True)
                return redirect(request.args.get("next") or url_for('profile_page'))
        except:
            return render_template("login.html", title="Авторизация", form=form)

    return render_template("login.html", title="Авторизация", form=form)


@app.route('/register/', methods=('POST', 'GET'))
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        try:
            hashed_password = generate_password_hash(password)

            user = Users(username=username, password=hashed_password)
            db.session.add(user)
            db.session.commit()
        except:
            db.session.rollback()
        session['logged_in'] = True

        return redirect(url_for('profile_page'))

    return render_template("register.html", title="Регистрация", form=form)


@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/add_review/', methods=('POST', 'GET'))
@login_required
def add_review():
    form = ReviewForm()
    categories = list(db.session.execute(db.select(Category.title)).scalars())

    if len(categories) > 0:
        form.category.choices = categories
    else:
        form.category.choices = 'Нет категорий'
    user = current_user.id
    if form.validate_on_submit():
        try:
            # В следующей строке берется id выбранной категории
            select_category = db.session.execute(
                db.select(Category.id).filter_by(title=form.category.data)).scalar_one()
            new_review = Reviews(title=form.title.data, rating=form.rating.data, review_text=form.review_text.data,
                                 category_id=select_category, user_id=user)
            db.session.add(new_review)
            db.session.commit()
        except:
            db.session.rollback()

        return redirect(url_for('reviews_page'))

    return render_template("add_review.html", title="Добавление отзыва", form=form)


@app.route('/add_category/', methods=('POST', 'GET'))
@login_required
def add_category():
    form = CategoryForm()
    if form.validate_on_submit():
        title = form.title.data
        try:
            category = Category(title=title)
            db.session.add(category)
            db.session.commit()
        except:
            db.session.rollback()

        return redirect(url_for('add_review'))

    return render_template("add_category.html", title="Добавление категории", form=form)


@app.route('/reviews/')
@login_required
def reviews_page():
    reviews = list(db.session.execute(db.select(Reviews)).scalars())
    category = list(db.session.execute(db.select(Category)).scalars())

    return render_template("reviews.html", title="Отзывы", reviews=reviews, category=category)


@app.route('/review/<int:id>/')
@login_required
def review(id):
    select_review = db.session.execute(db.select(Reviews).filter_by(id=id)).scalar_one()

    return render_template("review_page.html", title=select_review.title, review=select_review)


@app.route('/review/<int:id>/delete/', methods=['POST'])
@login_required
def review_delete(id):
    select_review_for_delete = db.session.execute(db.select(Reviews).filter_by(id=id)).scalar_one()
    db.session.delete(select_review_for_delete)
    db.session.commit()
    return redirect(url_for('reviews_page'))


@app.route('/category/<int:id>/')
@login_required
def category(id):
    select_category = db.session.execute(db.select(Category).filter_by(id=id)).scalar_one()
    category_reviews = select_category.review_id

    return render_template("category.html", title=select_category.title, category=select_category,
                           reviews=category_reviews)

# добавить сортировки по оценке, редактирование отзывов, категории и отзывы для каждого аккаунта отображать только свои
