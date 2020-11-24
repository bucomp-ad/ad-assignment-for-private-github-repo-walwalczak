from flask import Flask, jsonify, render_template, request
from flask_restful import Resource, reqparse
from google.auth.transport import requests
import google.oauth2.id_token
from pymongo import MongoClient


class Item(Resource):

    client = MongoClient("mongodb+srv://dbAdmin:Password01@cluster0.chzl0.mongodb.net/AdvancedDev?retryWrites=true&w=majority")
    db = client["AdvancedDev"]

    parser = reqparse.RequestParser() # controls what gets passed in
    parser.add_argument('price', type=float, required=True, help="This field is required")

    def get(self, name):
        item = Item.find_name(name)
        if item:
            return item
        return {'item': item}, 200 if item else 404

    @classmethod
    def find_name(cls, name):
        #client = MongoClient("mongodb+srv://dbAdmin:Password01@cluster0.chzl0.mongodb.net/AdvancedDev?retryWrites=true&w=majority")
        #db = client["AdvancedDev"]
        col = Item.db['items']

        query_name = col.find_one({"name": name})

        if query_name != None:
            return col.find_one({"name": name}, {'_id':0, 'name':1, 'price':1})
         # return col.find_one({"name": name})
            

    def post(self, name):
        print(Item.find_name(name))
        if Item.find_name(name):
            return {'message': f"An item with name '{name}' already exists."}, 400
        
        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}
        
        #client = MongoClient("mongodb+srv://dbAdmin:Password01@cluster0.chzl0.mongodb.net/AdvancedDev?retryWrites=true&w=majority")
        #db = client["AdvancedDev"]
        items = Item.db.items
        items.insert_one({'name': name, 'price': data['price']})

        return item, 201