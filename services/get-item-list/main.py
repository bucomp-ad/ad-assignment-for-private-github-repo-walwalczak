# start imports 
import pymongo
from bson.json_util import dumps
import os
from google.cloud import secretmanager

def item_list(request):

    secrets = secretmanager.SecretManagerServiceClient()
    name = "projects/468425812899/secrets/mongodb_url/versions/latest"
    url = secrets.access_secret_version({"name": name}).payload.data.decode("utf-8")
    
    if(not url):
        json_data = "{'error': 'Error: failed to get mongoDB connection string'}"
    else:
        # set-up client object and connect to cluster using url
        client = pymongo.MongoClient(url)

        # connect to the db
        db = client.AdvancedDev

        # get the complete of inventory items 
        my_cursor = db.items.find({})

        # convert the cursor to a python list
        list_cur = list(my_cursor)
        # print(list_cur)

        # dump the list into a string and return
        json_data = dumps(list_cur)

    return json_data
# end of cloud function 