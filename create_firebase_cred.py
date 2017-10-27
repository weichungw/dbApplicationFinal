
import json 

acc_key ={
    'type': 'service_account',
    'apiKey': "AIzaSyAqDEf5e_Jrb_IZTOAZqIymd0RamL0J8Is",
    'authDomain': "final-33b0a.firebaseapp.com",
    'databaseURL': "https://final-33b0a.firebaseio.com",
    'projectId': "final-33b0a",
    'storageBucket': "final-33b0a.appspot.com",
    'messagingSenderId': "502931069570"
}
with open('serviceAccountKey.json','w') as wfile:
    json.dump(acc_key,wfile,indent=4)
