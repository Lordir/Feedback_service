from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from flask_migrate import Migrate
from models import *

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)


@app.route('/')
def main_page():
    print(url_for("main_page"))
    return render_template("main_page.html", title="Main")


@app.route('/posts/<int:id>')
def posts(id):
    return f"Пользователь: {id}"
    # return render_template("main_page.html", title="Profile")


if __name__ == "__main__":
    app.run(debug=True)

# Искусственный контекст
# with app.test_request_context():
#     print(url_for("main_page"))
#     print(url_for("posts", id="1"))