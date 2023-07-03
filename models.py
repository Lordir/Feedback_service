from flask_sqlalchemy import SQLAlchemy
from flask import session
from flask_login import UserMixin

db = SQLAlchemy()


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(500), nullable=True)
    reviews = db.relationship('Reviews', backref='users')

    def __repr__(self):
        return f"User {self.username}"

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)


class Reviews(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True)
    rating = db.Column(db.Integer(), unique=True)
    review_text = db.Column(db.Text(), unique=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f"{self.title} - {self.rating}"


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True)
    review_id = db.relationship('Reviews', backref='category')

    def __repr__(self):
        return f"{self.title}"
