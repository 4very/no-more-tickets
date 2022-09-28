import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth, firestore
from firebase_admin.credentials import Certificate
from os import environ


config = {
    "authDomain": "troy-parking.firebaseapp.com",
    "projectId": "troy-parking",
    "storageBucket": "troy-parking.appspot.com",
    "apiKey": environ.get("FIREBASE_APIKEY"),
    "messagingSenderId": environ.get("FIREBASE_MESSAGING_SENDER_ID"),
    "appId": environ.get("FIREBASE_APP_ID"),
}

cred: Certificate = credentials.Certificate("private-key.json")

firebase_admin.initialize_app(cred, config)

auth = auth
firestore = firestore
