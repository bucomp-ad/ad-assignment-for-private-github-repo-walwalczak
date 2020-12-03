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
        item = Item.find_name(name)
        try:
            url = f'https://europe-west2-nps-demo-app.cloudfunctions.net/get-item/{name}'
            json_data = requests.get(url).json()
            return json_data, 201
        except:
            return {"message": "Unexpected error ocurred."}, 500

    def post(self, name):
        data = Item.parser.parse_args()
        try:
            url = 'https://europe-west2-nps-demo-app.cloudfunctions.net/post-item'
            json_data = requests.post(url, json = {'name': name, 'price': data['price']})
            return json_data.json() 
        except:
            return {"message": "Unexpected error ocurred."}, 500

    def put(self, name):
        data = Item.parser.parse_args()
        try:
            url = 'https://europe-west2-nps-demo-app.cloudfunctions.net/put-item'
            json_data = requests.put(url, json = {'name': name, 'price': data['price']})
            return json_data.json() 
        except:
            return {"message": "Unexpected error ocurred."}, 500

    def delete(self, name):
        if not Item.find_name(name):
            return {'message': 'This item does not exist.'}, 400
        
        try:
            item = {'name': name}
            items = db.items
            items.delete_one({'name': name})
            return {'message': 'Item deleted'}, 201
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


        