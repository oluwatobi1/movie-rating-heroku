from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse


app = Flask(__name__)
api = Api(app)

item = []

class Item(Resource):
    def get(self):
        return item, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name",
        type=str,
        required=True,
        choices=('one', 'two'),
        help="This field nust be one or two")
        print(parser.args)

        data = parser.parse_args()
        item.append(data['name'])
        return {'message':"successfull"}, 201


api.add_resource(Item, "/item")


if __name__ == "__main__":
    app.run(debug=True)