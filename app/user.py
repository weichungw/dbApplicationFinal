from flask_login import UserMixin
class User(UserMixin):
    def __init__(self,fuser,active=True):
        self.fuser = fuser
        self.username= None
        self.email= None
        self.password =None 
        self.refreshToken=None
        self.active =active
    

    def is_authenticated(self):
        #TODO
        return True
    def is_active(self):
        return self.active
    def is_anonymous(self):
        #TODO add flase condition
        return True 
    def get_id(self):
        return self.fuser['idToken']
    def get_auth_token(self):
        pass
    def __repr__(self):
        return "id:{}".format(self.fuser['idToken'])


