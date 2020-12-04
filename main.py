from flask import Flask, render_template, request
from flask_restful import Api, Resource
from item import Item, ItemList
from authenticate import check_token


app = Flask(__name__)
api = Api(app)

# item and item list routes
api.add_resource(ItemList, '/items')
api.add_resource(Item, '/item/<string:name>')

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/uploadfile')
@check_token
def upload_file():
    return render_template(
        'uploadfile.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)