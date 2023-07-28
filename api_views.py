import json
import operator

from flask import render_template
from flask_login import login_user, login_required, logout_user, current_user

from app import app
from models import *


@app.route('/api/reviews/')
@login_required
def reviews_api():
    user = db.session.execute(db.select(Users).filter_by(id=current_user.id)).scalar_one()
    reviews = user.reviews
    result = []
    for review in range(len(reviews)):
        result.append(reviews[review].serialize())
    result = json.dumps(result, ensure_ascii=False)

    return result


@app.route('/api/reviews/descending_sort_rating/')
@login_required
def reviews_descending_sort_rating_api():
    user = db.session.execute(db.select(Users).filter_by(id=current_user.id)).scalar_one()
    reviews = user.reviews
    sort_reviews = sorted(reviews, key=operator.attrgetter('rating'))

    result = []
    for review in range(len(sort_reviews)):
        result.append(sort_reviews[review].serialize())
    result = json.dumps(result, ensure_ascii=False)

    return result


@app.route('/api/reviews/ascending_sort_rating/')
@login_required
def reviews_ascending_sort_rating_api():
    user = db.session.execute(db.select(Users).filter_by(id=current_user.id)).scalar_one()
    reviews = user.reviews
    sort_reviews = sorted(reviews, key=operator.attrgetter('rating'), reverse=True)

    result = []
    for review in range(len(sort_reviews)):
        result.append(sort_reviews[review].serialize())
    result = json.dumps(result, ensure_ascii=False)

    return result


@app.route('/api/review/<int:id>/')
@login_required
def review_api(id):
    try:
        select_review = db.session.execute(db.select(Reviews).filter_by(id=id)).scalar_one()
        if select_review.user_id == current_user.id:
            result = select_review.serialize()
            result = json.dumps(result, ensure_ascii=False)
            return result
    except:
        return render_template('404.html')
    return render_template('404.html')


@app.route('/api/category/<int:id>/')
@login_required
def category_api(id):
    try:
        select_category = db.session.execute(db.select(Category).filter_by(id=id)).scalar_one()
        category_reviews = select_category.review_id
        category_reviews_at_current_user = []

        for element in category_reviews:
            if element.user_id == current_user.id:
                category_reviews_at_current_user.append(element)

        result = []
        for review in range(len(category_reviews_at_current_user)):
            result.append(category_reviews_at_current_user[review].serialize())

        result = json.dumps(result, ensure_ascii=False)

        return result
    except:
        return render_template('404.html')


@app.route('/api/category/<int:id>/descending_sort_rating/')
@login_required
def category_descending_sort_rating_api(id):
    try:
        select_category = db.session.execute(db.select(Category).filter_by(id=id)).scalar_one()
        category_reviews = select_category.review_id
        category_reviews_at_current_user = []
        for element in category_reviews:
            if element.user_id == current_user.id:
                category_reviews_at_current_user.append(element)
        sort_reviews = sorted(category_reviews_at_current_user, key=operator.attrgetter('rating'))

        result = []
        for review in range(len(sort_reviews)):
            result.append(sort_reviews[review].serialize())

        result = json.dumps(result, ensure_ascii=False)
        return result
    except:
        return render_template('404.html')


@app.route('/api/category/<int:id>/ascending_sort_rating/')
@login_required
def category_ascending_sort_rating_api(id):
    try:
        select_category = db.session.execute(db.select(Category).filter_by(id=id)).scalar_one()
        category_reviews = select_category.review_id
        category_reviews_at_current_user = []
        for element in category_reviews:
            if element.user_id == current_user.id:
                category_reviews_at_current_user.append(element)
        sort_reviews = sorted(category_reviews_at_current_user, key=operator.attrgetter('rating'), reverse=True)

        result = []
        for review in range(len(sort_reviews)):
            result.append(sort_reviews[review].serialize())

        result = json.dumps(result, ensure_ascii=False)
        return result
    except:
        return render_template('404.html')
