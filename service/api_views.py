import json
import operator
import logging

from flask import request, session, Blueprint
from flask_login import login_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash

from .models import *

LOG = logging.getLogger(__name__)
bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/reviews/')
@login_required
def reviews_api():
    user = db.session.execute(db.select(Users).filter_by(id=current_user.id)).scalar_one()
    reviews = user.reviews
    result = []
    for review in range(len(reviews)):
        result.append(reviews[review].serialize())
    result = json.dumps(result, ensure_ascii=False)

    return result


@bp.route('/reviews/descending_sort_rating/')
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


@bp.route('/reviews/ascending_sort_rating/')
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


@bp.route('/review/<int:id>/', methods=('GET', 'DELETE', 'PUT'))
@login_required
def review_api(id):
    if request.method == 'GET':
        try:
            select_review = db.session.execute(db.select(Reviews).filter_by(id=id)).scalar_one()
            if select_review.user_id == current_user.id:
                result = select_review.serialize()
                result = json.dumps(result, ensure_ascii=False)
                return result
            else:
                return json.dumps({"Ответ": "У вас нет прав для просмотра этого отзыва"}, ensure_ascii=False)
        except:
            return json.dumps({"Ответ": "Ошибка"}, ensure_ascii=False)

    if request.method == "DELETE":
        try:
            select_review_for_delete = db.session.execute(db.select(Reviews).filter_by(id=id)).scalar_one()
            if select_review_for_delete.user_id == current_user.id:
                db.session.delete(select_review_for_delete)
                db.session.commit()
                LOG.info(f"Пользователь {current_user.username} удалил отзыв {select_review_for_delete.title}")
                return json.dumps({"Ответ": "Отзыв удален"}, ensure_ascii=False)
            else:
                return json.dumps({"Ответ": "У вас нет прав для удаления этого отзыва"}, ensure_ascii=False)
        except:
            return json.dumps({"Ответ": "Ошибка удаления"}, ensure_ascii=False)

    if request.method == "PUT":
        request_data = request.get_json()
        try:
            select_review = db.session.execute(db.select(Reviews).filter_by(id=id)).scalar_one()

            if select_review.user_id == current_user.id:
                select_category = db.session.execute(
                    db.select(Category.id).filter_by(title=request_data['category'])).scalar_one()

                select_review.title = request_data['title']
                select_review.rating = request_data['rating']
                select_review.review_text = request_data['review_text']
                select_review.category_id = select_category

                db.session.add(select_review)
                db.session.commit()
                LOG.info(f"Пользователь {current_user.username} обновил отзыв {select_review.title}")
                return json.dumps({"Ответ": "Отзыв обновлен"}, ensure_ascii=False)

            else:
                return json.dumps({"Ответ": "У вас нет прав для изменения этого отзыва"}, ensure_ascii=False)
        except:
            db.session.rollback()
            return json.dumps({"Ответ": "Ошибка"}, ensure_ascii=False)


@bp.route('/category/<int:id>/')
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
        return json.dumps({"Ответ": "Ошибка"}, ensure_ascii=False)


@bp.route('/category/<int:id>/descending_sort_rating/')
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
        return json.dumps({"Ответ": "Ошибка"}, ensure_ascii=False)


@bp.route('/category/<int:id>/ascending_sort_rating/')
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
        return json.dumps({"Ответ": "Ошибка"}, ensure_ascii=False)


@bp.route('/login/', methods=['POST'])
def login_api():
    if current_user.is_authenticated:
        return json.dumps({"Ответ": "Вы уже авторизованы"}, ensure_ascii=False)

    request_data = request.get_json()
    username = request_data['username']
    password = request_data['password']

    try:
        user = db.session.execute(db.select(Users).filter_by(username=username)).scalar_one()
        if user and check_password_hash(user.password, password):
            session['logged_in'] = True
            login_user(user, remember=True)
            LOG.info(f"Пользователь {current_user.username} вошел в аккаунт")
            return json.dumps({"Ответ": "Успешно"}, ensure_ascii=False)
    except:
        return json.dumps({"Ответ": "Неверные данные или ошибка"}, ensure_ascii=False)


@bp.route('/register/', methods=['POST'])
def register_api():
    if current_user.is_authenticated:
        return json.dumps({"Ответ": "Вы уже авторизованы"}, ensure_ascii=False)

    request_data = request.get_json()
    username = request_data['username']
    password = request_data['password']
    if len(username) < 4 or len(password) < 4:
        return json.dumps({"Ответ": "Длина username и password должна быть от 4 символов"}, ensure_ascii=False)

    try:
        hashed_password = generate_password_hash(password)
        user = Users(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        session['logged_in'] = True
        LOG.info(f"Прошел регистрацию пользователь {user.username}")
        return json.dumps({"Ответ": "Успешно"}, ensure_ascii=False)
    except:
        db.session.rollback()
        return json.dumps({"Ответ": "Ошибка"}, ensure_ascii=False)


@bp.route('/add_review/', methods=['POST'])
@login_required
def add_review_api():
    user = current_user.id
    request_data = request.get_json()

    try:
        id_category = db.session.execute(db.select(Category.id).filter_by(title=request_data['category'])).scalar_one()
        new_review = Reviews(title=request_data['title'], rating=request_data['rating'],
                             review_text=request_data['review_text'], category_id=id_category, user_id=user)
        db.session.add(new_review)
        db.session.commit()
        LOG.info(f"Пользователь {current_user.username} успешно добавил отзыв: {new_review.title}")
        return json.dumps({"Ответ": "Отзыв добавлен"}, ensure_ascii=False)
    except:
        db.session.rollback()
        return json.dumps({"Ответ": "Ошибка"}, ensure_ascii=False)


@bp.route('/add_category/', methods=['POST'])
@login_required
def add_category_api():
    request_data = request.get_json()
    if len(request_data['title']) < 4:
        return json.dumps({"Ответ": "Длина названия должна быть от 4 символов"}, ensure_ascii=False)

    try:
        category = Category(title=request_data['title'])
        db.session.add(category)
        db.session.commit()
        LOG.info(f"Пользователь {current_user.username} успешно добавил категорию: {category.title}")
        return json.dumps({"Ответ": "Категория добавлена"}, ensure_ascii=False)
    except:
        db.session.rollback()
        return json.dumps({"Ответ": "Ошибка"}, ensure_ascii=False)
