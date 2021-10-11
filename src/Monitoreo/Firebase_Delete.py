from firebase import firebase
from dotenv import load_dotenv
import os

load_dotenv()



FIREBASE = os.getenv('F_EndPoint')

# esta parte esta hecha por mi
firebase = firebase.FirebaseApplication(FIREBASE, None)

pedro = firebase.delete ('/Monitoreo/Listin Diario', None) 
print(pedro)