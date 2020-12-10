from flask import Flask, jsonify, request
from flask_restful import Resource, reqparse
from authenticate import check_token
import requests
import json

class TrelloBoard(Resource):
    @check_token
    # create public board with default list
    def post(self, name):
        try:
            url = f'https://api.trello.com/1/boards/'
            query = {
                'key':'a1ed8530e742c0328ff8e6c7846bcfde',
                'token':'257c5590aae375a02cbb81b8e950036504f186e8ceb95756cd73351fe1981837',
                'name':f'{name}',
                'defaultLists':'true',
                'prefs_permissionLevel':'public'
            }
            response = requests.post(url, params=query)
            print(f'Response: {response.json()}')
            return response.json() 
        except:
            return {"message": "Unexpected error ocurred."}, 500
        