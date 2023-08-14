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

    "При вводе неправильного логина, обработка исключения"
    auth.logout()
    response = client.post('/login/', data={"username": "test222", "password": "password"}, follow_redirects=True)
    assert response.request.path == '/login/'


def test_register(client):
    assert client.get('/register/').status_code == 200

    response = client.post('/register/', data={"username": "test2", "password": "password2"}, follow_redirects=True)
    assert response.request.path == '/login/'

    response = client.post('/register/', data={"username": "test2", "password": "password2"}, follow_redirects=True)
    assert response.request.path == '/register/'


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

    "Проверка, что категория не добавится, если ввести второй раз одного и тоже название"
    response = client.post('/add_category/', data={"title": "test_category"}, follow_redirects=True)
    assert response.request.path == '/add_category/'

    "Проверка некорректности формы"
    response = client.post('/add_category/', data={"title": "1"}, follow_redirects=True)
    assert response.request.path == '/add_category/'


def test_view_reviews(client, auth):
    auth.login()
    response = client.get('/reviews/')
    assert "test - 3" in response.data.decode()

    response2 = client.get('/reviews/descending_sort_rating/')
    assert "test - 3" in response2.data.decode()

    response3 = client.get('/reviews/ascending_sort_rating/')
    assert "test - 3" in response3.data.decode()


def test_review_id(client, auth):
    auth.login()
    response = client.get('/review/1/')
    assert "Название: test" in response.data.decode()

    "Проверка ввода несуществующего id"
    response = client.get('/review/300/')
    assert "Данная страница не существует или недоступна!" in response.data.decode()


def test_review_update(client, auth):
    auth.login()
    response = client.get('/review/1/update')
    assert "test" in response.data.decode()

    client.post('/review/1/update',
                data={"title": "test99", "rating": 3, "review_text": "", "category_id": 1, "user_id": 1},
                follow_redirects=True)

    response2 = client.get('/review/1/update')
    assert "test99" in response2.data.decode()

    "При вводе некорректных данных ничего не обновится"
    client.post('/review/1/update',
                data={"title": "", "rating": 3, "review_text": "", "category_id": 1, "user_id": 1},
                follow_redirects=True)
    response3 = client.get('/review/1/update')
    assert "test99" in response3.data.decode()

    "Проверка ввода несуществующего id"
    response = client.post('/review/6/update',
                           data={"title": "test99", "rating": 3, "review_text": "", "category_id": 1, "user_id": 1},
                           follow_redirects=True)
    assert "Данная страница не существует или недоступна!" in response.data.decode()


def test_view_category(client, auth):
    auth.login()
    response = client.get('/category/1/')
    assert "test99 - 3" in response.data.decode()
    response = client.get('/category/7575/')
    assert "Данная страница не существует или недоступна!" in response.data.decode()

    response2 = client.get('/category/1/descending_sort_rating/')
    assert "test99 - 3" in response2.data.decode()
    response2 = client.get('/category/444/descending_sort_rating/')
    assert "Данная страница не существует или недоступна!" in response2.data.decode()

    response3 = client.get('/category/1/ascending_sort_rating/')
    assert "test99 - 3" in response3.data.decode()
    response3 = client.get('/category/666/ascending_sort_rating/')
    assert "Данная страница не существует или недоступна!" in response3.data.decode()


