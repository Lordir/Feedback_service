from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from flask_migrate import Migrate
from flask_login import LoginManager
from models import *

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)

from views import *


@login_manager.user_loader
def load_user(id):
    return Users.get(id)


if __name__ == "__main__":
    app.run(debug=True)

# Искусственный контекст
# with app.test_request_context():
#     print(url_for("main_page"))
#     print(url_for("posts", id="1"))
