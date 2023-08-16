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
    client.put('/api/review/1/', json={"title": "test_api_review_2", "rating": 8, "review_text": "test_text",
                                       "category": "test_cat_api"})
    response = client.get('/api/review/1/')
    assert json.loads(response.data) == {"id": 1, "title": "test_api_review_2", "rating": 8, "review_text": "test_text"}
