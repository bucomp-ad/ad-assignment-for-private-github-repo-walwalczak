from flask import Flask, render_template
from flask_restful import Api, Resource
from item import Item, ItemList
from user import Register, SignIn


app = Flask(__name__)
api = Api(app)


api.add_resource(ItemList, '/items')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(Register, '/register')
api.add_resource(SignIn, '/signin')


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)