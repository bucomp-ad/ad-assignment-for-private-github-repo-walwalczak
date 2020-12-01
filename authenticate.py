from google.auth.transport import requests
import google.oauth2.id_token
from flask import request
from functools import wraps
import firebase_admin
from firebase_admin import auth, credentials
import pyrebase
from flask_restful import reqparse, Resource


cred = credentials.Certificate("nps-demo-app-firebase-adminsdk-aysya-cbbdd7dca9.json")
firebase_admin.initialize_app(cred)
config = {
    "apiKey": "AIzaSyC1lWoEQGssAUgMOGXQPr-BudMpZEQE3xc",
    "authDomain": "nps-demo-app.firebaseapp.com",
    "databaseURL": "https://nps-demo-app.firebaseio.com",
    "storageBucket": "nps-demo-app.appspot.com",
    "messagingSenderId": "468425812899",
    "appId": "1:468425812899:web:cf670e802f13db00bec816",
    "measurementId": "G-D5W2BRF78P"
    }
firebase = pyrebase.initialize_app(config)

def check_token(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        firebase_request_adapter = requests.Request()
        id_token = request.cookies.get("token")
        # get claims
        claims = google.oauth2.id_token.verify_firebase_token(
                id_token, firebase_request_adapter)

        if id_token == None:
            return {'message': 'No token provided'}, 400
        try:
            claims['admin']
        except:
            return {'message':'Insufficient permissions.'}, 400
        return f(*args, **kwargs)
    return wrap


class Register(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str,
    required=True)

    parser.add_argument('password', type=str,
    required=True)

    def post(self):
        data = Register.parser.parse_args()

        user_email = data['email']
        user_password = data['password']
        user = firebase.auth().create_user_with_email_and_password(user_email, user_password)

        auth.set_custom_user_claims(user['localId'], {'admin': True})
        firebase.auth().send_email_verification(user['idToken'])

        return {"message": f"{user['email']} has been registered."}, 201