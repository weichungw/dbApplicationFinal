from firebase import firebase

fbapp = firebase.FirebaseApplication('https://final-33b0a.firebaseio.com/',authentication=None)
authentication = firebase.FirebaseAuthentication('C-0yZeab9BVSdTCl2vKDw4_D',
        'weichunw@usc.edu')
print(authentication.extra)
user = authentication.get_user()
print(user.firebase_auth_token)
#fbapp.authentication = authentication
result= fbapp.get('/Users', None )
print(result) 
