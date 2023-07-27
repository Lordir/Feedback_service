import operator
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
    user = db.session.execute(db.select(Users).filter_by(id=current_user.id)).scalar_one()
    reviews = user.reviews
    category = list(db.session.execute(db.select(Category)).scalars())

    return render_template("reviews.html", title="Отзывы", reviews=reviews, category=category)


@app.route('/reviews/descending_sort_rating/')
@login_required
def reviews_descending_sort_rating():
    user = db.session.execute(db.select(Users).filter_by(id=current_user.id)).scalar_one()
    reviews = user.reviews
    sort_reviews = sorted(reviews, key=operator.attrgetter('rating'))
    category = list(db.session.execute(db.select(Category)).scalars())

    return render_template("reviews.html", title="Отзывы", reviews=sort_reviews, category=category)


@app.route('/reviews/ascending_sort_rating/')
@login_required
def reviews_ascending_sort_rating():
    user = db.session.execute(db.select(Users).filter_by(id=current_user.id)).scalar_one()
    reviews = user.reviews
    sort_reviews = sorted(reviews, key=operator.attrgetter('rating'), reverse=True)
    category = list(db.session.execute(db.select(Category)).scalars())

    return render_template("reviews.html", title="Отзывы", reviews=sort_reviews, category=category)


@app.route('/review/<int:id>/')
@login_required
def review(id):
    try:
        select_review = db.session.execute(db.select(Reviews).filter_by(id=id)).scalar_one()
        if select_review.user_id == current_user.id:
            return render_template("review_page.html", title=select_review.title, review=select_review)
    except:
        return render_template('404.html')
    return render_template('404.html')


@app.route('/review/<int:id>/update', methods=('POST', 'GET'))
@login_required
def review_update(id):
    try:
        select_review = db.session.execute(db.select(Reviews).filter_by(id=id)).scalar_one()
        categories = list(db.session.execute(db.select(Category.title)).scalars())
        form = ReviewForm(obj=select_review)
        if len(categories) > 0:
            form.category.choices = categories
        else:
            form.category.choices = 'Нет категорий'
        if form.validate_on_submit():
            try:
                # В следующей строке берется id выбранной категории
                select_category = db.session.execute(
                    db.select(Category.id).filter_by(title=form.category.data)).scalar_one()

                select_review.title = form.title.data
                select_review.rating = form.rating.data
                select_review.review_text = form.review_text.data
                select_review.category_id = select_category

                db.session.add(select_review)
                db.session.commit()
            except:
                db.session.rollback()
        if select_review.user_id == current_user.id:
            return render_template("review_update.html", title=select_review.title, form=form, review=select_review)
    except:
        return render_template('404.html')
    return render_template('404.html')


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
    try:
        select_category = db.session.execute(db.select(Category).filter_by(id=id)).scalar_one()
        category_reviews = select_category.review_id
        category_reviews_at_current_user = []
        for element in category_reviews:
            if element.user_id == current_user.id:
                category_reviews_at_current_user.append(element)

        return render_template("category.html", title=select_category.title, category=select_category,
                               reviews=category_reviews_at_current_user)
    except:
        return render_template('404.html')


@app.route('/category/<int:id>/descending_sort_rating/')
@login_required
def category_descending_sort_rating(id):
    try:
        select_category = db.session.execute(db.select(Category).filter_by(id=id)).scalar_one()
        category_reviews = select_category.review_id
        category_reviews_at_current_user = []
        for element in category_reviews:
            if element.user_id == current_user.id:
                category_reviews_at_current_user.append(element)
        sort_reviews = sorted(category_reviews_at_current_user, key=operator.attrgetter('rating'))

        return render_template("category.html", title=select_category.title, category=select_category,
                               reviews=sort_reviews)
    except:
        return render_template('404.html')


@app.route('/category/<int:id>/ascending_sort_rating/')
@login_required
def category_ascending_sort_rating(id):
    try:
        select_category = db.session.execute(db.select(Category).filter_by(id=id)).scalar_one()
        category_reviews = select_category.review_id
        category_reviews_at_current_user = []
        for element in category_reviews:
            if element.user_id == current_user.id:
                category_reviews_at_current_user.append(element)
        sort_reviews = sorted(category_reviews_at_current_user, key=operator.attrgetter('rating'), reverse=True)

        return render_template("category.html", title=select_category.title, category=select_category,
                               reviews=sort_reviews)
    except:
        return render_template('404.html')

