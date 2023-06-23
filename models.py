from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(500), nullable=True)
    reviews = db.relationship('Reviews', backref='users')

    def __repr__(self):
        return f"<User {self.username}>"


class Reviews(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True)
    rating = db.Column(db.Integer(), unique=True)
    review_text = db.Column(db.Text(), unique=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f"<Review {self.title} - {self.rating}>"


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True)
    review_id = db.relationship('Reviews', backref='category')

    def __repr__(self):
        return f"<Category {self.title}>"
