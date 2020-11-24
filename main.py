import datetime

from flask import Flask, render_template, request
from flask_restful import Resource, Api
from google.auth.transport import requests
from google.cloud import datastore
import google.oauth2.id_token

firebase_request_adapter = requests.Request()

datastore_client = datastore.Client()

app = Flask(__name__)
api = Api(app)


items = []


class Item(Resource):
    def get(self, name):
        query = datastore_client.query(kind='item')
        print(query.fetch())
        #return query

    def post(self, name):
        item = datastore.Entity(key=datastore_client.key('item'))
        item.update({
            'name': name,
            'price': 12.00
        })
        return item # notifies app that this has happened

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