from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    username = StringField('Логин: ', validators=[DataRequired(), Length(min=4)])
    password = StringField('Пароль: ', validators=[DataRequired(), Length(min=4)])
    submit = SubmitField("Войти")


class RegisterForm(FlaskForm):
    username = StringField('Логин: ', validators=[DataRequired(), Length(min=4)])
    password = StringField('Пароль: ', validators=[DataRequired(), Length(min=4)])
    submit = SubmitField("Регистрация")
