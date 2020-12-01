from flask import Flask, render_template, request
from flask_restful import Api, Resource
from resources.item import Item, ItemList
from authenticate import Register

app = Flask(__name__)
api = Api(app)

api.add_resource(ItemList, '/items')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(Register, '/register')

@app.route('/')
def root():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)