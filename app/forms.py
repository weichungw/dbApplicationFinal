from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, TextField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])

    #remember_me = BooleanField('remember_me', default=False)

class SignUpForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
    repeatpassword = StringField('repeatpassword', validators=[DataRequired()])
