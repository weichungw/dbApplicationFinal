import os

from flask import Flask

from flask_login import LoginManager
from config import basedir, FIREBASE_CONFIG

#from firebase import firebase
#import firebase_admin

import pyrebase
from firebase_admin import credentials

app = Flask(__name__)
app.config.from_object('config')
#db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view="account"

#firebase = firebase.FirebaseApplication('https://final-33b0a.firebaseio.com/',None)
cred = credentials.Certificate('final-33b0a-firebase-adminsdk-vjuqw-d474b38d4b.json')
fbapp = pyrebase.initialize_app(FIREBASE_CONFIG)
auth = fbapp.auth()
db = fbapp.database()

from app import views#, models

