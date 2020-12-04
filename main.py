from flask import Flask, render_template, request, redirect
from flask_restful import Api, Resource
from item import Item, ItemList
from google.auth.transport import requests as google_requests
import google.oauth2.id_token
import requests

from requests import put, get, delete, post


app = Flask(__name__)
api = Api(app)

# item and item list routes
api.add_resource(ItemList, '/items')
api.add_resource(Item, '/item/<string:name>')

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/uploadfile')
def upload_file():
    # Verify Firebase auth.
    id_token = request.cookies.get("token")
    error_message = None
    claims = None
    times = None
    # print("id_token:" + id_token)
    if id_token:
        try:
            firebase_request_adapter = google_requests.Request()
            claims = google.oauth2.id_token.verify_firebase_token(
                id_token, firebase_request_adapter)
            
        except ValueError as exc:
            # This will be raised if the token is expired or any other
            # verification checks fail.
            error_message = str(exc)
            # print("Error: " + error_message)
    else:
        # print("No valid auth token set.")
        return redirect("/")

    return render_template(
        'uploadfile.html', user_data=claims, error_message=error_message)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)