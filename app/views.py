from flask import render_template, flash, redirect
from flask import session, url_for, request ,g
from flask_login import login_user, logout_user, current_user, login_required

from app import app, fbapp, auth, db
from app import lm

from .user import User

from .forms import LoginForm, SignUpForm 


@app.route('/')
@app.route('/index')
def index():
    user = {'nickname':'miguel'}
    posts =[
            {
                'author' :{'nickname':'John'},
                'body':'Deautiful day in Portland'
                },
            {
                'author':{'nickname':'Susan'},
                'body':'The Avengers movie was so cool!'
                }

            ]
    return render_template('index.html',
            title='Home',
            user=user,
            posts=posts) 

@app.route('/home', methods=['GET'])
def main():
    app.logger.debug('')
    return render_template('home.html')

@app.route('/feed', methods=['GET'])
def feed():
    return render_template('feed.html')
        
@app.route('/account', methods=['GET','POST'])
def account():
    lform = LoginForm()
    sform = SignUpForm()
    error =""
    app.logger.debug('enter account page')

    return render_template('account.html',
            lform=lform,
            sform=sform,
            error=error)

@app.route('/signin',methods=['GET','POST'])
def signin():
    app.logger.debug('Enter login function')
    lform = LoginForm()
    if lform.validate_on_submit():
        print('valid login form')
        try:
            email = lform.email.data
            password = lform.password.data
            fuser = auth.sign_in_with_email_and_password(email, password)
            user= User(fuser)
        except :
            app.logger.error = 'User not found, please double check your email'
            return redirect('account')
        login_user(user)
        return redirect('home')

    return redirect('account') 

@app.route('/signup', methods=['GET','POST'])
def signup():
    app.logger.debug('Enter signup function')
    sform = SignUpForm()
    if sform.validate_on_submit():
        print('valid signup form')
        username = sform.username.data
        email = sform.email.data
        password = sform.password.data
        repeatpassword = sform.repeatpassword.data
        if password == repeatpassword:
            fuser=auth.create_user_with_email_and_password(email, password)
            put_data ={ 
                        'password':password,
                        'email':email,
                        'username':username,
                        'id':fuser['idToken']
                        }

            db.child('Users').child(username).set(put_data)
            app.logger.debug('Sign up {} success... '.format(username))
            return redirect('account')
    return redirect('account')

@app.route('/secret',methods=['GET'])
@login_required
def secret():
    return render_template('secret.html')

@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect('index')


@lm.user_loader
def load_user(id):
    app.logger.debug('enter user_loader id:{}'.format(id))
    user =None
    try: 
        fuser=auth.get_account_info(id)
        user=User(fuser)
    except :
        print('google authentication fail')
    return user 

#@lm.request_loader
#def request_loader(request):
#    username = request.form.get('username')
#    u=User.query.filter_by(username=username).first()
#    user.is_authenticated = request.form['password'] == u.password
#    return user

        
