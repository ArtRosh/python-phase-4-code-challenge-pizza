#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


class Index(Resource):
    def get(self):
        return {"message": "Code challenge"}, 200
    

class Restaurants(Resource):
    def get(self):
        restaurants = [
            r.to_dict(only=("address", "name", "id"))
            for r in Restaurant.query.all()
            ]

        return restaurants, 200

    
api.add_resource(Index, "/")
api.add_resource(Restaurants, "/restaurants")



if __name__ == "__main__":
    app.run(port=5555, debug=True)
