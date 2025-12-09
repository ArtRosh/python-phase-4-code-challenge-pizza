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
    

class RestaurantById(Resource):
    def get(self, id):
        restaurant_by_id = Restaurant.query.filter_by(id=id).first()
        if not restaurant_by_id:
            return {"error": "Restaurant not found"}, 404
        else:
            return restaurant_by_id.to_dict(), 200
        
    def delete(self,id):
        restaurant_by_id = Restaurant.query.filter_by(id=id).first()
        if not restaurant_by_id:
            return {"error": "Restaurant not found"}, 404
        else:
            db.session.delete(restaurant_by_id)
            db.session.commit()
            return {}, 204
        

class Pizzas(Resource):
    def get(self):
        pizzas = [
            p.to_dict(only=("id", "ingredients", "name")) 
            for p in Pizza.query.all()
            ]

        return pizzas, 200
    

class RestaurantPizzas(Resource):
    def post(self):
        data = request.get_json()

        try:
            new_record = RestaurantPizza(
                price=data.get("price"),
                pizza_id=data.get("pizza_id"),
                restaurant_id=data.get("restaurant_id")
            )
            db.session.add(new_record)
            db.session.commit()
        except ValueError as e:
            db.session.rollback()
            return {"errors": ["validation errors"]}, 400
        
        return new_record.to_dict(), 201


    
api.add_resource(Index, "/")
api.add_resource(Restaurants, "/restaurants")
api.add_resource(RestaurantById, "/restaurants/<int:id>")
api.add_resource(Pizzas, "/pizzas")
api.add_resource(RestaurantPizzas, "/restaurant_pizzas")


if __name__ == "__main__":
    app.run(port=5555, debug=True)
