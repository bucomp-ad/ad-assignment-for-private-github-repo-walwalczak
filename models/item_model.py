from mongodb import client, db

class ItemModel:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def json(self):
        return {'name': self.name, 'price': self.price}

    @classmethod
    def find_name(cls, name):
        items = db['items']

        item = items.find_one({"name": name}, {'_id':0, 'name':1, 'price':1})
        if item:
            return cls(item['name'], item['price'])
    
    def insert(self):
        #data = Item.parser.parse_args()
        #item = {'name': name, 'price': data['price']}
            
        items = db['items']
        items.insert_one({'name': self.name, 'price': self.price})