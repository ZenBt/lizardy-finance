from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    pwd = PasswordField('Password', validators=[DataRequired()])

class RegForm(LoginForm):
    pwd = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=40)])
    

class AddTag(FlaskForm):
    tag = StringField('Category', validators=[DataRequired()])


class AddExpense(FlaskForm):
    name = StringField('ExpenseName', validators=[DataRequired()])
    description = TextAreaField('Description')
    cost = IntegerField('Price', validators=[DataRequired()], render_kw={'min':'1', 'max':'10000000000'})
    tag = SelectField('Category', coerce=int)  


class AddTag(FlaskForm):
    tag = StringField('Category', validators=[DataRequired()])     
