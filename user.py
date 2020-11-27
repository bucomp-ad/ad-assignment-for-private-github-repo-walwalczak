from flask_restful import Resource, reqparse
from flask import Flask, jsonify, render_template, request, make_response
import pyrebase
from firebase_admin import auth
from functools import wraps
from flask_restful import Resource

class User:
    def __init__(self, uid, email, password):
        self.uidd = uid
        self.email = email
        self.password = password

    def find_by_email(self, email):
        try:
            user = auth.get_user_by_email(email)
            return user
        except:
            return {"message":"User not found"}

    def find_by_uid(self, uid):
        try:
            user = auth.get_user(uid)
        except:
            return {"message":"User not found"}


config = {
    "apiKey": "AIzaSyC1lWoEQGssAUgMOGXQPr-BudMpZEQE3xc",
    "authDomain": "nps-demo-app.firebaseapp.com",
    "databaseURL": "https://nps-demo-app.firebaseio.com",
    "storageBucket": "nps-demo-app.appspot.com",
    "messagingSenderId": "468425812899",
    "appId": "1:468425812899:web:cf670e802f13db00bec816",
    "measurementId": "G-D5W2BRF78P"
    }

# init firebase
firebase = pyrebase.initialize_app(config)
db = firebase.database()

def check_token(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if request.headers.get('authorization') == None:
            return {'message': 'No token provided'},400
        try:
            user = auth.verify_id_token(request.headers['authorization'])
            request.user = user
        except:
            return {'message':'Invalid token provided.'},400
        return f(*args, **kwargs)
    return wrap

class SignIn(Resource):
    def post(self):
        try:
            email = request.form.get('email')
            password = request.form.get('password')
            user = firebase.auth().sign_in_with_email_and_password(email, password)
            jwt = user['idToken']
            print(request.headers.get('authorization'))
            return {'token': jwt}, 200
        except:
            return {'message': 'There was an error logging in'},400


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

        return {"message": f"{user['email']} has been registered."}, 201
