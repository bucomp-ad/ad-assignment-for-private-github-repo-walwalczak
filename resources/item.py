from flask import Flask, jsonify, request
from flask_restful import Resource, reqparse
from mongodb import client, db
from authenticate import check_token


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help="This field is required")
    
    @check_token
    def get(self, name):
        item = Item.find_name(name)
        if item:
            return item
        return {'item': item}, 200 if item else 404

    @classmethod
    def find_name(cls, name):
        col = db['items']
        query_name = col.find_one({"name": name})

        if query_name != None:
            return col.find_one({"name": name}, {'_id':0, 'name':1, 'price':1})

    def post(self, name):
        data = Item.parser.parse_args()
        if Item.find_name(name):
            return {'message': f"An item with name '{name}' already exists."}, 400
        try:
            item = {'name': name, 'price': data['price']}
            
            items = db.items
            items.insert_one({'name': name, 'price': data['price']})
        except:
            return {"message": "Unexpected error ocurred."}, 500

        return item, 201

    def put(self, name):
        data = Item.parser.parse_args()
        item = Item.find_name(name)
        if item:
            updated_item = {'$set' : {'name': name, 'price': data['price']}}
        
            items = db.items
            items.update_one(item, updated_item)

            #get updated item
            item = Item.find_name(name)
            return item, 201
        try:
            item = {'name': name, 'price': data['price']}
            items = db.items
            items.insert_one({'name': name, 'price': data['price']})
            return item, 201
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
    def get(self):
        items = db['items']
        items_dict = {}
        items_dict['items'] = []

        for item in items.find({}, {'_id':0, 'name':1, 'price':1}):
            items_dict['items'].append(item)

        return items_dict, 201


