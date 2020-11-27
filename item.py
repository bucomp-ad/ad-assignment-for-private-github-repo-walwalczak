from flask import Flask, jsonify, render_template, request
from flask_restful import Resource, reqparse
from mongodb import client, db
from flask_jwt import JWT, jwt_required
#from security import authenticate, identity
from user import check_token

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help="This field is required")

    @check_token
    def get(self, name):
        item = Item.find_name(name)
        if item:
            return item
        return {'item': item}, 200 if item else 404

    def find_name(self, name):
        col = db['items']
        query_name = col.find_one({"name": name})

        if query_name != None:
            return col.find_one({"name": name}, {'_id':0, 'name':1, 'price':1})

    def post(self, name):
        if Item.find_name(name):
            return {'message': f"An item with name '{name}' already exists."}, 400
        
        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}
        
        items = db.items
        items.insert_one({'name': name, 'price': data['price']})

        return item, 201