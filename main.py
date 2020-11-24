import datetime
from pymongo import MongoClient
from flask import Flask, jsonify, render_template, request
from flask_restful import Api
from google.auth.transport import requests
import google.oauth2.id_token
from item import Item

firebase_request_adapter = requests.Request()

app = Flask(__name__)
api = Api(app)
        
#api.add_resource(ItemList, '/items')
api.add_resource(Item, '/item/<string:name>')

@app.route('/')
def root():
    # Verify Firebase auth.
    id_token = request.cookies.get("token")
    error_message = None
    claims = None

    if id_token:
        try:
            claims = google.oauth2.id_token.verify_firebase_token(
                id_token, firebase_request_adapter)

        except ValueError as exc:
            # This will be raised if the token is expired or any other
            # verification checks fail.
            error_message = str(exc)

    return render_template(
        'index.html',
        user_data=claims, error_message=error_message)

if __name__ == '__main__':

    app.run(host='127.0.0.1', port=8080, debug=True)