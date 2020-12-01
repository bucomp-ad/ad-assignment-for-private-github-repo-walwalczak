from flask import Flask, jsonify, request
from flask_restful import Resource, reqparse
from mongodb import client, db
from authenticate import check_token
from models.item_model import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help="This field is required")
    
    @check_token
    def get(self, name):
        item = ItemModel.find_name(name)
        if item:
            return item.json()
        return {'item': item}, 200 if item else 404

    def post(self, name):
        
        if ItemModel.find_name(name):
            return {'message': f"An item with name '{name}' already exists."}, 400

        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'])
        
        try:
            item.insert()
        except:
            return {"message": "Unexpected error ocurred."}, 500

        return item.json(), 201

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_name(name)
        updated_item = ItemModel(name, data['price'])

        if item:
            updated_item = {'$set' : {'name': updated_item.name, 'price': updated_item.price}}
        
            items = db['items']
            items.update_one(item.json(), updated_item)

            # Update variable with new details
            updated_item = ItemModel.find_name(name)
            return updated_item.json(), 201
        try:
            item = ItemModel(name, data['price'])
            item.insert()
            
            return item.json(), 201
        except:
            return {"message": "Unexpected error ocurred."}, 500

    def delete(self, name):
        if not ItemModel.find_name(name):
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


