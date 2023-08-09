from flask_admin import Admin
from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from flask_migrate import Migrate
from flask_login import LoginManager
from logging.config import dictConfig

from .admin import *

load_dotenv()

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    },
        "file": {
            "class": "logging.FileHandler",
            "filename": "flask.log",
            "formatter": "default",
        },
    },
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi', 'file']
    }

})


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

    from service.models import db, Users

    db.init_app(app)
    migrate = Migrate(app, db)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    login_manager.login_message = "Авторизуйтесь для доступа"

    admin = Admin(app, name='Feedback service admin', template_mode='bootstrap3')
    admin.add_view(MainModelView(Users, db.session))
    admin.add_view(ReviewsModelView(Reviews, db.session))
    admin.add_view(MainModelView(Category, db.session))

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # from service import views
    # from api_views import *

    @login_manager.user_loader
    def load_user(id):
        user = db.session.execute(db.select(Users).filter_by(id=id)).scalar_one()
        return user

    from . import views, api_views
    app.register_blueprint(views.bp)
    app.register_blueprint(api_views.bp)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

# Искусственный контекст
# with app.test_request_context():
#     print(url_for("main_page"))
#     print(url_for("posts", id="1"))
