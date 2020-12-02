from google.auth.transport import requests
import google.oauth2.id_token
from flask import request
from functools import wraps

def check_token(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        firebase_request_adapter = requests.Request()
        id_token = request.cookies.get("token")
        error_message = None
        claims = None
        id_token = request.cookies.get("token")

        if id_token == None:
            return {'message': 'No token provided'}, 400
        try:
            claims = google.oauth2.id_token.verify_firebase_token(
                id_token, firebase_request_adapter)
        except:
            return {'message':'Invalid token provided.'}, 400
        return f(*args, **kwargs)
    return wrap