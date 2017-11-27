import os
from flask import render_template, flash, redirect
from flask import session, url_for, request ,g
#from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename

from app import app, fbapp, auth, db, storage
#from app import lm

from datetime import datetime
from .user import User
from .forms import LoginForm, SignUpForm, PostPushForm

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
def home():
    if 'userToken' not in session:
        return redirect(url_for('account'))
        
    print(session['userToken'])
    uemail = session['userToken']['email']
    user = db.child('Users/').order_by_child('email').equal_to(uemail).get().val()
    print('current user\n')
    for username, uinfo in user.items():
        uname =username
        #upids = [pid for pid in uinfo['posts']]
        #utoken= uinfo['id'] # redundent
        #uemail=uinfo['email'] #redundent
    session['username']=uname
    app.logger.debug('Enter home')
    pform = PostPushForm()
    post_ids=db.child('Users/{}/posts'.format(uname))\
        .order_by_key().limit_to_last(3).get().val()
    print(post_ids)
    myposts=[]
    if post_ids:
        for pid in reversed(post_ids):
            p=db.child('Posts/{}/'.format(pid)).get().val()
            p["avtar_url"]=db.child('Users/{}/avtar'.format(p['author'])).get().val()
            myposts.append(p)
    print('Myposts:\n')
    print(myposts)
    

    return render_template('home.html', pform=pform, posts=myposts)

@app.route('/pushpost', methods =['POST'])
def pushpost():
    pform = PostPushForm()
    app.logger.debug('Pushpost request')
    if pform.validate_on_submit():
        username = session['username']
        # recieve post
        app.logger.debug('Valid post push')
        context = pform.context.data

        print('get context:\n{}'.format(context))
        f= pform.photo.data
        filename = secure_filename(f.filename)
        print('get filename:\n{}'.format(filename))

        filepath = os.path.join(app.config['UPLOAD_FOLDER'],filename)
        f.save(filepath)  # TODO either implement my put or delete file after upload

        #push post
        new_post = {
                'pic_url':"",
                'context': context,
                'author': username,
                'liker':{},
                'time':datetime.now().strftime('%Y-%m-%d %H:%M')
                }
        post_id=db.child('Posts/').push(new_post)

        storage.child("Posts/{}".format(post_id['name'])).put(filepath)
        pic_url = storage.child("Posts/{}".format(post_id['name'])).get_url(None)
        db.child('Posts/{}'.format(post_id['name'])).update({"pic_url":pic_url})

        db.child('Users/{}/posts/{}'.format(username,post_id['name'])).set(True)

    return redirect(url_for('home'))

@app.route('/feed', methods=['GET'])
def feed():
    if "userToken" not in session:
        return redirect(url_for('account'))
    username = session['username']
    post_ids=db.child('Posts/').order_by_key().limit_to_last(6).get()
    print(post_ids)
    print(post_ids.val())
    feedposts=[]
    if post_ids:
        for pid in post_ids.each():
            p=pid.val()
            if p['author']==username:
                continue
            p["avtar_url"] =db.child('Users/{}/avtar'.format(p['author'])).get().val()
            feedposts.append(p)
    if len(feedposts):
        feedposts.reverse()

    return render_template('feed.html',posts=feedposts)

@app.route('/')
@app.route('/account', methods=['GET','POST'])
def account():
    lform = LoginForm()
    sform = SignUpForm()
    error =""
    app.logger.debug('enter account page')
    if 'userToken' in session:
        print('Fucked')

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
            print('fuser')
            print(fuser)
            session['userToken']=fuser
            #user= User(fuser)
        except :
            app.logger.error = 'User not found, please double check your email'
            return redirect('account')
        #login_user(user)
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
        f = sform.avtar.data
        if password == repeatpassword:
            # cache file
            print('cache file')
            filename = secure_filename(f.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'],filename)
            f.save(filepath)
            # upload avtar
            print('upload avtar')
            storage.child("Avtars/{}".format(username)).put(filepath)
            avtar_url = storage.child("Avtars/{}".format(username)).get_url(None)
            
            # create user
            print('create user')
            fuser=auth.create_user_with_email_and_password(email, password)
            #avtar_url=storage.child("Avtar/defaultAvtar.jpg").get_url(None)
            put_data ={ 
                        'password':password,
                        'email':email,
                        'username':username,
                        'id':fuser['idToken'],
                        'posts':{},
                        'avtar':avtar_url
                        }

            db.child('Users').child(username).set(put_data)
            app.logger.debug('Sign up {} success... '.format(username))
            return redirect('home')

    for e in sform.errors:
        print(e)

    return redirect('account')


@app.route('/logout', methods=['GET'])
def logout():
    session.pop('userToken',None)
    return redirect('account')

@app.route('/newpost', methods=['GET'])
def newpost():
    return render_template('Postimg.html')

@app.route('/video', methods=['GET'])
def vedio():
    return render_template('video.html')

#@lm.user_loader
#def load_user(id):
#    app.logger.debug('enter user_loader id:{}'.format(id))
#    user =None
#    try: 
#        fuser=auth.get_account_info(id)
#        user=User(fuser)
#    except :
#        print('google authentication fail')
#    return user 

#@lm.request_loader
#def request_loader(request):
#    username = request.form.get('username')
#    u=User.query.filter_by(username=username).first()
#    user.is_authenticated = request.form['password'] == u.password
#    return user


