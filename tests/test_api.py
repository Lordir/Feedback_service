import json

from werkzeug.security import generate_password_hash

from service.models import *


def test_api_reviews(client, auth, app):
    "Добавление категории, пользователя и отзыва в БД"
    user = Users(username="test_api", password=generate_password_hash("password"))
    category = Category(title="test_cat_api")
    review = Reviews(title="test_api_review", rating=9, review_text='test_text', category_id=1, user_id=1)
    with app.app_context():
        db.session.add(user)
        db.session.add(category)
        db.session.add(review)
        db.session.commit()

    auth.login(username="test_api", password="password")
    response = client.get('/api/reviews/')
    assert json.loads(response.data) == [{'id': 1, 'rating': 9, 'review_text': 'test_text', 'title': 'test_api_review'}]

    response = client.get('/api/reviews/descending_sort_rating/')
    assert json.loads(response.data) == [{'id': 1, 'rating': 9, 'review_text': 'test_text', 'title': 'test_api_review'}]

    response = client.get('/api/reviews/ascending_sort_rating/')
    assert json.loads(response.data) == [{'id': 1, 'rating': 9, 'review_text': 'test_text', 'title': 'test_api_review'}]


def test_get_review(client, auth):
    auth.login(username="test_api", password="password")
    response = client.get('/api/review/1/')
    assert json.loads(response.data) == {"id": 1, "title": "test_api_review", "rating": 9, "review_text": "test_text"}

    "Проверка ошибки при запросе несуществующего отзыва"
    response = client.get('/api/review/2/')
    assert json.loads(response.data) == {'Ответ': 'Ошибка'}


def test_put_review(client, auth):
    auth.login(username="test_api", password="password")
    response = client.put('/api/review/1/', json={"title": "test_api_review_2", "rating": 8, "review_text": "test_text",
                                                  "category": "test_cat_api"})
    assert json.loads(response.data) == {"Ответ": "Отзыв обновлен"}

    response = client.get('/api/review/1/')
    assert json.loads(response.data) == {"id": 1, "title": "test_api_review_2", "rating": 8, "review_text": "test_text"}


def test_get_api_category(client, auth):
    auth.login(username="test_api", password="password")
    response = client.get('/api/category/1/')
    assert json.loads(response.data) == [
        {"id": 1, "title": "test_api_review_2", "rating": 8, "review_text": "test_text"}]
    response = client.get('/api/category/100/')
    assert json.loads(response.data) == {'Ответ': 'Ошибка'}

    response = client.get('/api/category/1/descending_sort_rating/')
    assert json.loads(response.data) == [
        {"id": 1, "title": "test_api_review_2", "rating": 8, "review_text": "test_text"}]
    response = client.get('/api/category/100/descending_sort_rating/')
    assert json.loads(response.data) == {'Ответ': 'Ошибка'}

    response = client.get('/api/category/1/ascending_sort_rating/')
    assert json.loads(response.data) == [
        {"id": 1, "title": "test_api_review_2", "rating": 8, "review_text": "test_text"}]
    response = client.get('/api/category/100/ascending_sort_rating/')
    assert json.loads(response.data) == {'Ответ': 'Ошибка'}


def test_api_login(client, auth):
    response = client.post('/api/login/', json={'username': "test_api", 'password': "password"})
    assert json.loads(response.data) == {"Ответ": "Успешно"}

    "Попытка повторной авторизации"
    response = client.post('/api/login/', json={'username': "test_api", 'password': "password"})
    assert json.loads(response.data) == {"Ответ": "Вы уже авторизованы"}

    auth.logout()
    "Неверные данные"
    response = client.post('/api/login/', json={'username': "test_apihhhh", 'password': "password"})
    assert json.loads(response.data) == {"Ответ": "Неверные данные или ошибка"}


def test_api_register(client, app):
    response = client.post('/api/register/', json={'username': "test_api_reg", 'password': "password"})
    assert json.loads(response.data) == {"Ответ": "Успешно"}

    response = client.post('/api/register/', json={'username': "t", 'password': "password"})
    assert json.loads(response.data) == {"Ответ": "Длина username и password должна быть от 4 символов"}

    response = client.post('/api/register/', json={'username': "test_api_reg", 'password': "password"})
    assert json.loads(response.data) == {"Ответ": "Ошибка"}

    "Проверка, что пользователь успешно зарегистрирован"
    with app.app_context():
        added_user = Users.query.filter_by(username='test_api_reg').first()

        assert added_user is not None
        assert added_user.username == "test_api_reg"


def test_api_add_category(client, auth, app):
    auth.login(username="test_api", password="password")
    response = client.post('/api/add_category/', json={'title': 'test_api_cat'})
    assert json.loads(response.data) == {"Ответ": "Категория добавлена"}

    response = client.post('/api/add_category/', json={'title': 'g'})
    assert json.loads(response.data) == {"Ответ": "Длина названия должна быть от 4 символов"}

    "Проверка, что категория добавлена"
    with app.app_context():
        added_category = Category.query.filter_by(title='test_api_cat').first()

        assert added_category is not None
        assert added_category.title == "test_api_cat"


def test_api_add_review(client, auth, app):
    auth.login(username="test_api", password="password")
    response = client.post('/api/add_review/',
                           json={"title": "test_api_add", "rating": 1, "review_text": "text",
                                 "category": "test_cat_api"})
    assert json.loads(response.data) == {"Ответ": "Отзыв добавлен"}

    "Ввод некорректных данных"
    response = client.post('/api/add_review/',
                           json={"title": "test_api_add", "rating": 1, "review_text": "text",
                                 "category": "аа"})
    assert json.loads(response.data) == {"Ответ": "Ошибка"}

    "Проверка, что отзыв добавлен"
    with app.app_context():
        added_review = Reviews.query.filter_by(title='test_api_add').first()

        assert added_review is not None
        assert added_review.title == 'test_api_add'


def test_api_delete(client, auth, app):
    auth.login(username="test_api", password="password")
    response = client.delete('/api/review/2/')
    assert json.loads(response.data) == {"Ответ": "Отзыв удален"}

    response = client.get('/api/review/2/')
    assert json.loads(response.data) == {"Ответ": "Ошибка"}
