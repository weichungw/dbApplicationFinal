#from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(64))
    email = db.Column(db.String(120), index=True, unique=True)
    is_authenticated = False
    
    #one2many magic line
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    
    @property
    def is_authenticated(self):
        return self.is_authenticated 

    @property
    def is_active(self):
        return True
    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(slef.id) #py2
        except NameError:
            return str(self.id) #py3
    def __repr__(self):
        return '<User %r>' %(self.username)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp=db.Column(db.DateTime)
    #author
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)
