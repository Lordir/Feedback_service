from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import flask_login
from flask import url_for, request, redirect

from .models import *


class MainModelView(ModelView):

    def is_accessible(self):
        return flask_login.current_user.is_authenticated and flask_login.current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))


class ReviewsModelView(MainModelView):
    column_list = (Reviews.id, Reviews.title, Reviews.rating, Reviews.review_text, Reviews.category_id, Reviews.user_id)

    # inline_models = (Category, Users)
    # column_editable_list = [Category.id, Users.id]

    def is_accessible(self):
        return flask_login.current_user.is_authenticated and flask_login.current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))

