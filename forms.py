from wsgiref.validate import validator
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    pwd = PasswordField('Password', validators=[DataRequired()])

class RegForm(LoginForm):
    pwd = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=40)])
