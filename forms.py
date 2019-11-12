from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Email, Length


class SignupForm(FlaskForm):
    name = StringField('Username', validators=[DataRequired(), Length(max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Sign up')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Log in')


class PostForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired(), Length(max=80)])
    content = TextAreaField('Contenido')
    submit = SubmitField('Enviar')
