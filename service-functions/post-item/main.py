# start imports 
import pymongo
from bson.json_util import dumps
import os
from google.cloud import secretmanager
import requests
import json

def post_item(request):
    secrets = secretmanager.SecretManagerServiceClient()
    name = "projects/468425812899/secrets/mongodb_url/versions/latest"
    url = secrets.access_secret_version({"name": name}).payload.data.decode("utf-8")

    item = request.get_json(silent=True)
    item_name = item['name']

    client = pymongo.MongoClient(url)
    # connect to the db
    db = client.AdvancedDev

    my_cursor = db.items.find_one({"name": item_name})

    if my_cursor:
        return {'message': f"An item with name '{item_name}' already exists."}, 400
    try:
        db.items.insert_one(item)
    except:
        return {"message": "Unexpected error ocurred."}, 500

    return {"message": "Item uploaded successfully"}, 201
# end of cloud function 