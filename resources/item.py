from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class ItemsList(Resource):

    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}

        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = 'SELECT * FROM items'
        # result = cursor.execute(query)
        # items = []
        # for row in result:
        #     items.append({'name': row[0], 'price': row[1]})
        # connection.close()
        # return {'items': items}


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help='This field is important')
    parser.add_argument('store_id',
                        type=float,
                        required=True,
                        help='This field is important')

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:  # is not none
            return item.json()
        return {'message': 'Item not in list'}

    def post(self, name):

        if ItemModel.find_by_name(name):
            return {'message': f'Item {name} Already in database'}, 400
        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'], data['store_id'])

        try:
            item.save_to_db()
        except:
            return {'Message': 'An error occurred'}, 500
        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'item deleted'}

    def put(self, name):

        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, data['price'], data['store_id'])
        else:
            item.price = data['price']
        item.save_to_db()
        return item.json()
