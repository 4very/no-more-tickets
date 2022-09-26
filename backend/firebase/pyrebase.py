import pyrebase
from os import environ
from pprint import pprint





config = {

  "authDomain": "troy-parking.firebaseapp.com",
  "projectId": "troy-parking",
  "storageBucket": "troy-parking.appspot.com",
  "databaseURL": "https://troy-parking-default-rtdb.firebaseio.com/",

  "apiKey": environ.get("FIREBASE_APIKEY"),
  "messagingSenderId": environ.get("FIREBASE_MESSAGING_SENDER_ID"),
  "appId": environ.get("FIREBASE_APP_ID")

}

firebase = pyrebase.initialize_app(config)


auth = firebase.auth()
firestore  = firebase.database()