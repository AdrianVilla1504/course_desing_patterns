from flask_restful import Resource, reqparse
import json
from flask import request
from utils.database_connection import DatabaseConnection

def is_valid_token(token):
    return token == 'abcd1234'

class ProductsResource(Resource):
    def __init__(self):

        self.db = DatabaseConnection('db.json')
        self.db.connect()

        self.products = self.db.get_products()
        self.parser = reqparse.RequestParser()
        
    def get(self, product_id=None):
        args = self.parser.parse_args()
        token = request.headers.get('Authorization')
        category_filter = request.args.get('category')

        if not token:
            return { 'message': 'Unauthorized acces token not found'}, 401

        if not is_valid_token(token):
            return { 'message': 'Unauthorized invalid token'}, 401

        if category_filter:
            filtered_products = [p for p in self.products if p['category'].lower() == category_filter.lower()]
            return filtered_products 
        
        if product_id is not None:
            product = next((p for p in self.products if p['id'] == product_id), None)
            if product is not None:
                return product
            else:
                return {'message': 'Product not found'}, 404
              
        return self.products

    def post(self):
        token = request.headers.get('Authorization')
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help='Name of the product')
        parser.add_argument('category', type=str, required=True, help='Category of the product')
        parser.add_argument('price', type=float, required=True, help='Price of the product')

        args = parser.parse_args()
        new_product = {
            'id': len(self.products) + 1,
            'name': args['name'],
            'category': args['category'],
            'price': args['price']
        }

        self.products.append(new_product)
        self.db.add_product(new_product)
        return {'mensaje': 'Product added', 'product': new_product}, 201


