from flask_restful import Resource, reqparse
import json
from flask import request
from utils.database_connection import DatabaseConnection

def is_valid_token(token):
    return token == 'abcd1234'


class FavoritesResource(Resource):
    def __init__(self):
        self.db = DatabaseConnection('favorites.json')
        self.db.connect()

        self.favorites = self.db.get_favorites()

    def get(self):
        token = request.headers.get('Authorization')
        
        if not token:
            return {'message': 'Unauthorized access token not found'}, 401

        if not is_valid_token(token):
            return {'message': 'Unauthorized invalid token'}, 401

        return self.db.get_favorites(), 200

    def post(self):
        token = request.headers.get('Authorization')
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=int, required=True, help='User ID')
        parser.add_argument('product_id', type=int, required=True, help='Product ID')
        if not token:
            return { 'message': 'Unauthorized acces token not found'}, 401

        if not is_valid_token(token):
           return { 'message': 'Unauthorized invalid token'}, 401


        args = parser.parse_args()
        new_favorite = {
            'user_id': args['user_id'],
            'product_id': args['product_id']
        }

        self.favorites.append(new_favorite)
        self.db.add_favorite(new_favorite)
        return {'message': 'Product added to favorites', 'favorite': new_favorite}, 201

    def delete(self):
        token = request.headers.get('Authorization')
        if not token:
            return { 'message': 'Unauthorized acces token not found'}, 401

        if not is_valid_token(token):
            return { 'message': 'Unauthorized invalid token'}, 401

        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=int, required=True, help='User ID')
        parser.add_argument('product_id', type=int, required=True, help='Product ID')

        args = parser.parse_args()
        user_id = args['user_id']
        product_id = args['product_id']

        # Encuentra y elimina el producto de favoritos
        self.favorites = [favorite for favorite in self.favorites
                        if not (favorite['user_id'] == user_id and favorite['product_id'] == product_id)]
        self.db.save_favorites(self.favorites)

        return {'message': 'Product removed from favorites'}, 200
