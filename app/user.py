from flask_login import UserMixin
class User(UserMixin):
    def __init__(self,id , username='anthony', password='secret',  active=True):
        self.id =str(id)
        self.name =username+str(id)
        self.password = password 
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
        return self.id
    def get_auth_token(self):
        pass
    def __repr__(self):
        return "{} {} {}".format(self.id,self.name,self.password)


