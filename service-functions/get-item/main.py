import pymongo
import os
from google.cloud import secretmanager
import requests
from flask import jsonify

def get_item(request):
    secrets = secretmanager.SecretManagerServiceClient()
    name = "projects/468425812899/secrets/mongodb_url/versions/latest"
    url = secrets.access_secret_version({"name": name}).payload.data.decode("utf-8")
    
    if(not url):
        json_data = "{'error': 'Error: failed to get mongoDB connection string'}", 500
    else:
        item_name = request.view_args['path']
        # set-up client object and connect to cluster using url
        client = pymongo.MongoClient(url)

        # connect to the db
        db = client.AdvancedDev
        item = db.items.find_one({"name": item_name}, {'_id':0, 'name':1, 'price':1})
        if item:
            return jsonify(item), 201
        else:
            return {'message': f'Item {item_name} has not been found.'}, 400
# end of cloud function 