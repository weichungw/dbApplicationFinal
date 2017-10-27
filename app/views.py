from flask import render_template, flash, redirect
from flask import session, url_for, request ,g
from flask_login import login_user, logout_user, current_user, login_required
from app import app, fbapp, auth, db
#from app import firebase, lm

from .forms import LoginForm, SignUpForm 
#from .models import User


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


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    sform = SignUpForm()
    if sform.validate_on_submit():
        app.logger.debug('signup the mother fucker')
        username = sform.username.data
        password = sform.password.data
        email = sform.email.data
        put_data ={ 
                    'password':password,
                    'email':email 
                    }
        auth.create_user_with_email_and_password(email, password)
        db.child('Users').child(username).set(put_data)
        return redirect('login')

    return render_template('signup.html',
            form=sform)
        
@app.route('/login',methods=['GET','POST'])
def login():
    lform = LoginForm()
    error =""
    if lform.validate_on_submit():
        print('fuck ya')
        try:
            email = lform.email.data
            password = lform.password.data
            user = auth.sign_in_with_email_and_password(email, password)
        except:
            error = 'User not found, please double check your email'
            return render_template('login.html',
                    form=lform,
                    error=error) 

        app.logger.debug(user)
        return redirect('secret')

    return render_template('login.html',
            form=lform,
            error=error)

@app.route('/secret',methods=['GET'])
def secret():
    return render_template('secret.html')

@app.route('/logout', methods=['GET'])
def logout():
    return redirect('index')


#@lm.user_loader
#def load_user(id):
#    app.logger.debug('enter user_loader')
#    return User.query.get(int(id))

#@lm.request_loader
#def request_loader(request):
#    username = request.form.get('username')
#    u=User.query.filter_by(username=username).first()
#    user.is_authenticated = request.form['password'] == u.password
#    return user

        

#@app.route('/login',methods=['GET','POST'])
#def login():
#    #if g.user is not None and g.user.is_authenticated:
#    #    return redirect(url_for('index'))
#    form=LoginForm()
#    error=None
#    if form.validate_on_submit():
#        users=User.query.all()
#        app.logger.debug(str(form.username))
#        app.logger.debug(type(form.username))
#        user = User.query.filter_by(username=form.username.data).first()
#        if user:
#            if login_user(user):
#                user.is_authenticated =True
#                app.logger.debug('Logged in user %s', user.username)
#                flash('Logged insuccessfully.')
#                return redirect(url_for('secret'))
#        error = 'Invalid username or password.'
#        session['remember_me'] = form.remember_me.data
#        #flash('Login requested for OpenID="%s", remember_me%s' %
#        #        (form.openid.data, str(form.remember_me.data)))
#        #return redirect('/index')
#
#    return render_template('login.html',
#            title='Sign In',
#            form=form,
#            error=error,
#            providers=app.config['OPENID_PROVIDERS']
#            )
