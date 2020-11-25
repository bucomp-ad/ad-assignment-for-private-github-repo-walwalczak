from pymongo import MongoClient
from flask import Flask, jsonify, render_template, request
from flask_restful import Api
import pyrebase
from item import Item

app = Flask(__name__)

#var firebaseConfig = {
#    apiKey: "AIzaSyC1lWoEQGssAUgMOGXQPr-BudMpZEQE3xc",
#    authDomain: "nps-demo-app.firebaseapp.com",
#    databaseURL: "https://nps-demo-app.firebaseio.com",
#    projectId: "nps-demo-app",
#    storageBucket: "nps-demo-app.appspot.com",
#    messagingSenderId: "468425812899",
#    appId: "1:468425812899:web:cf670e802f13db00bec816",
#   measurementId: "G-D5W2BRF78P"
#  };


config = {
"apiKey": "AIzaSyC1lWoEQGssAUgMOGXQPr-BudMpZEQE3xc",
"authDomain": "nps-demo-app.firebaseapp.com",
"databaseURL": "https://nps-demo-app.firebaseio.com",
"storageBucket": "nps-demo-app.appspot.com"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

api = Api(app)

#api.add_resource(ItemList, '/items')
api.add_resource(Item, '/item/<string:name>')

@app.route('/', methods=['GET', 'POST'])
def root():
    # auth.create_user_with_email_and_password('email@email.com', 'password')

    login_failed = 'Please check your credentials'
    
    if request.method == 'POST':
        email = request.form['name']
        password = request.form['pass']
        try:
            auth.sign_in_with_email_and_password(email, password)
            return 'Login successful'
        except:
            return render_template('index.html', lf=login_failed)
        
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)