import pytest
from flask_migrate import upgrade as flask_migrate_upgrade

from service import create_app
from service.models import db


@pytest.fixture(scope="session")
def app():
    app = create_app(test_config=True)
    app.config.update({"TESTING": True, })
    app.config['WTF_CSRF_ENABLED'] = False

    # app_context = app.app_context()
    # app_context.push()

    with app.app_context():
        db.create_all()
        db.session.commit()

    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope="function")
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='password'):
        return self._client.post(
            '/api/login/',
            json={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/logout/')


@pytest.fixture
def auth(client):
    return AuthActions(client)
