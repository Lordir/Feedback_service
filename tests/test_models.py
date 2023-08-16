from werkzeug.security import generate_password_hash

from service.models import *


def test_model_users(app):
    user = Users(username="test", password=generate_password_hash("password"))

    "Добавление пользователя в БД"
    with app.app_context():
        db.session.add(user)
        db.session.commit()
    "Проверка, что пользователь добавлен, пароль захэшировался, поле username верно, пользователь не является админом"
    with app.app_context():
        added_user = Users.query.filter_by(username='test').first()

        assert added_user is not None
        assert added_user.username == "test"
        assert added_user.password != "password"
        assert added_user.is_admin is False
        assert str(added_user) == "User test"
        assert added_user.is_authenticated() is True
        assert added_user.get_id() == "2"


def test_model_category(app):
    category = Category(title="test_title")

    "Добавление категории в БД"
    with app.app_context():
        db.session.add(category)
        db.session.commit()
    "Проверка, что категория добавлена"
    with app.app_context():
        added_category = Category.query.filter_by(title='test_title').first()

        assert added_category is not None
        assert added_category.title == "test_title"
        assert str(added_category) == "test_title"


def test_model_reviews(app):
    review = Reviews(title="test", rating=3, review_text='', category_id=2, user_id=2)

    "Добавление отзыва БД"
    with app.app_context():
        db.session.add(review)
        db.session.commit()
    "Проверка, что отзыв добавлен"
    with app.app_context():
        added_review = Reviews.query.filter_by(title='test').first()

        assert added_review is not None
        assert added_review.review_text == ''
        assert str(added_review) == "test - 3"
        assert added_review.serialize()['rating'] == 3
