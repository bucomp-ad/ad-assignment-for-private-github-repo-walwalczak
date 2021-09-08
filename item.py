from flask import Flask, jsonify, request
from flask_restful import Resource, reqparse
from authenticate import check_token
import requests
import json

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help="This field is required")
    
    @check_token
    def get(self, name):
        try:
            url = f'https://europe-west2-nps-demo-app.cloudfunctions.net/get-item/{name}'
            json_data = requests.get(url).json()
            return json_data, 201
        except:
            return {"message": "Unexpected error ocurred."}, 500

    @check_token
    def post(self, name):
        data = Item.parser.parse_args()
        try:
            url = 'https://europe-west2-nps-demo-app.cloudfunctions.net/post-item'
            json_data = requests.post(url, json = {'name': name, 'price': data['price']})
            return json_data.json() 
        except:
            return {"message": "Unexpected error ocurred."}, 500

    @check_token
    def put(self, name):
        data = Item.parser.parse_args()
        try:
            url = 'https://europe-west2-nps-demo-app.cloudfunctions.net/put-item'
            json_data = requests.put(url, json = {'name': name, 'price': data['price']})
            return json_data.json() 
        except:
            return {"message": "Unexpected error ocurred."}, 500
    
    @check_token
    def delete(self, name):
        try:
            url = f'https://europe-west2-nps-demo-app.cloudfunctions.net/delete-item/{name}'
            json_data = requests.get(url).json()
            return json_data, 201
        except:
            return {"message": "Unexpected error ocurred."}, 500

class ItemList(Resource):
    @check_token
    def get(self):
        try:
            url = 'https://europe-west2-nps-demo-app.cloudfunctions.net/item-list'
            json_data = requests.get(url).json()
            return json_data, 201
        except:
            return {"message": "Unexpected error ocurred."}, 500
