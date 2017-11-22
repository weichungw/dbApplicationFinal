from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, TextField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField,FileRequired, FileAllowed

ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'gif', 'png']

class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])

    #remember_me = BooleanField('remember_me', default=False)

class SignUpForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
    repeatpassword = StringField('repeatpassword', validators=[DataRequired()])
    avtar = FileField('avtar',
                      validators=[DataRequired(),
                        FileAllowed(ALLOWED_EXTENSIONS, 'Images only!') 
                      ])


class PostPushForm(FlaskForm):
    context = TextField('context', validators=[DataRequired()])
    photo = FileField('photo',
                      validators=[DataRequired(),
                        FileAllowed(ALLOWED_EXTENSIONS, 'Images only!') 
                      ])

