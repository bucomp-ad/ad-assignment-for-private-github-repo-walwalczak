# start imports 
import requests
import json

# end imports

# Service Cloud function to get a list of inventory items
# the passed request object should contain the url of the mesh service to use. 
def get_item_list(request):
    request_json = request.get_json(silent=True)
    print(f'request_json: {request.get_json(silent=True)}')

    request_args = request.args
    print(f'request_args: {request.args}')
    # check to see which data source to use and switch to the approrpiate mesh service. 
    if(request_json and 'source' in request_json):
        # if JSON passed - use API tester to test
        mesh_source = request_json['source']
    else:
        # if querystring passed - helps with testing quickly
        mesh_source = request.args.get('source')
    print(f'mesh_source: {request.args.get("source")}')
    # naive implementation - as code will need updating to add/edit meshSources. What would be a better way to implement this?
    if(mesh_source=='mongo'):
        url = 'https://europe-west2-nps-demo-app.cloudfunctions.net/item-list' 
    else:
        pass
        #url = "https://europe-west2-adfirstapp-286716.cloudfunctions.net/service_mesh_get_inventory_list_file"
    # get the data
    json_data = requests.get(url).content
    # return the data
    return json_data
# end of cloud function 