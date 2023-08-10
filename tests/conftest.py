import pytest
from flask_migrate import upgrade as flask_migrate_upgrade

from service import create_app
from service.models import db


@pytest.fixture(scope="session")
def app():
    app = create_app(test_config=True)
    app.config.update({"TESTING": True, })

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

# @pytest.fixture(scope="session")
# def db(app, request):
#     """Session-wide test database."""
#
#     def teardown():
#         _db.drop_all()
#
#     _db.app = app
#
#     flask_migrate_upgrade(directory='migrations')
#     request.addfinalizer(teardown)
#     return _db
#
#
# @pytest.fixture(scope="function")
# def session(db, request):
#     db.session.begin_nested()
#
#     def commit():
#         db.session.flush()
#         # patch commit method
#
#     old_commit = db.session.commit
#     db.session.commit = commit
#
#     def teardown():
#         db.session.rollback()
#         db.session.close()
#         db.session.commit = old_commit
#
#     request.addfinalizer(teardown)
#     return db.session
