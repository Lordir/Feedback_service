from service.models import *


def test_main_page(client):
    assert client.get('/').status_code == 200


def test_profile(client, auth):
    assert client.get('/profile/').status_code == 302
    auth.login()
    assert client.get('/profile/').status_code == 200


def test_login(client, auth):
    assert client.get('/login/').status_code == 200

    "Проверка авторизации и редиректа после нее"
    response = client.post('/login/', data={"username": "test", "password": "password"}, follow_redirects=True)
    assert response.request.path == '/profile/'

    response = client.get('/login/', follow_redirects=True)
    "Проверка редиректа в профиль, если пользователь уже авторизован"
    assert len(response.history) == 1
    assert response.request.path == '/profile/'

    "При вводе неправильного пароля"
    auth.logout()
    response = client.post('/login/', data={"username": "test", "password": "password1"}, follow_redirects=True)
    assert response.request.path == '/login/'


def test_register(client):
    assert client.get('/register/').status_code == 200

    response = client.post('/register/', data={"username": "test2", "password": "password2"}, follow_redirects=True)
    assert response.request.path == '/login/'


def test_logout(client):
    response = client.get('/logout/', follow_redirects=True)
    assert response.request.path == '/login/'


# def test_add_review(client, app, auth):
#     assert client.get('/add_review/').status_code == 302
#     auth.login()
#
#     response = client.post('/add_review/',
#                            data={"title": "test2", "rating": 5, "review_text": "gg", "category_id": 1, "user_id": 1},
#                            follow_redirects=True)
#     assert response.request.path == '/reviews/'
#
#     "Проверка, что отзыв добавлен"
#     with app.app_context():
#         added_review = Reviews.query.filter_by(title='test2').first()
#
#         assert added_review is not None
#         assert added_review.rating == 5


def test_add_category(client, app, auth):
    auth.login()
    response = client.post('/add_category/', data={"title": "test_category"}, follow_redirects=True)
    assert response.request.path == '/add_review/'

    "Проверка, что категория добавлена"
    with app.app_context():
        added_category = Category.query.filter_by(title='test_category').first()

        assert added_category is not None
        assert added_category.title == "test_category"
