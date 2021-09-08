# start imports 
import pymongo
import os
from google.cloud import secretmanager
import requests
from flask import jsonify

def put_item(request):
    secrets = secretmanager.SecretManagerServiceClient()
    name = "projects/468425812899/secrets/mongodb_url/versions/latest"
    url = secrets.access_secret_version({"name": name}).payload.data.decode("utf-8")
    
    item = request.get_json(silent=True)
    item_name = item['name']

    client = pymongo.MongoClient(url)
    # connect to the db
    db = client.AdvancedDev
    # check for item
    my_cursor = db.items.find_one({"name": item_name}, {'_id':0, 'name':1, 'price':1})
    
    # update if item exists
    if my_cursor:
        updated_item = {'$set' : item}
        db.items.update_one(my_cursor, updated_item)
        # get updated cursor value
        my_cursor = db.items.find_one({"name": item_name}, {'_id':0, 'name':1, 'price':1})
        return jsonify(my_cursor), 201
    else:
        try:
            db.items.insert_one(item)
            # get updated cursor value
            my_cursor = db.items.find_one({"name": item_name}, {'_id':0, 'name':1, 'price':1})
            return jsonify(my_cursor), 201
        except:
            return {"message": "Unexpected error ocurred."}, 500
# end of cloud function