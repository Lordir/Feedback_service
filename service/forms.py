from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, InputRequired, NumberRange, Optional


class LoginForm(FlaskForm):
    username = StringField('Логин: ', validators=[DataRequired(), Length(min=4)])
    password = StringField('Пароль: ', validators=[DataRequired(), Length(min=4)])
    submit = SubmitField("Войти")


class RegisterForm(FlaskForm):
    username = StringField('Логин: ', validators=[DataRequired(), Length(min=4)])
    password = StringField('Пароль: ', validators=[DataRequired(), Length(min=4)])
    submit = SubmitField("Регистрация")


class CategoryForm(FlaskForm):
    title = StringField('Название: ', validators=[DataRequired(), Length(min=4)])
    submit = SubmitField("Добавить категорию")


class ReviewForm(FlaskForm):
    title = StringField('Название: ', validators=[DataRequired(), Length(min=4)])
    rating = IntegerField('Оценка: ', validators=[InputRequired(), NumberRange(min=1, max=10)])
    review_text = TextAreaField('Отзыв: ', validators=[Optional(), Length(max=500)])
    category = SelectField('Категория: ')
    user_id = IntegerField('Идентификатор создателя')
    submit = SubmitField("Добавить отзыв")
