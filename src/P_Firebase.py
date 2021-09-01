import firebase_admin
from firebase_admin import credentials, db, exceptions
import joel
import os
from dotenv import load_dotenv


load_dotenv()

databaseURL = os.getenv('F_EndPoint')

F_credentials = os.getenv('F_FirebaseCredentials')


cred_obj = credentials.Certificate(F_credentials)
firebase_admin.initialize_app(cred_obj, {
	'databaseURL': databaseURL 
	})



ref = db.reference('/')

ref.set(joel.lamama())

ref.set({
        'Web Scraping': 
            {
                'box001': {
                    'color': 'red',
                    'width': 1,
                    'height': 3,
                    'length': 2
                },
                'box002': {
                    'color': 'green',
                    'width': 1,
                    'height': 2,
                    'length': 3
                },
                'box003': {
                    'color': 'yellow',
                    'width': 3,
                    'height': 2,
                    'length': 1
                }
            }
        })




""" #estoo es para guardar listas de datos
ref = db.reference('boxes')
ref.push({
    'color': 'purple',
    'width': 7,
    'height': 8,
    'length': 6
})
"""


""" 
with open("book_info.json", "r") as f:
	file_contents = json.load(f)
ref.set(file_contents) """




















ref = db.reference('boxes')
box_ref = ref.child('box001')
box_ref.update({
    'color': 'blue'
})