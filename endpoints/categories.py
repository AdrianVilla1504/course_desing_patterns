from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import json
from utils.database_connection import DatabaseConnection

def is_valid_token(token):
    return token == 'abcd1234'

class CategoriesResource(Resource):
    def __init__(self):

        self.db = DatabaseConnection('db.json')
        self.db.connect()

        self.categories_data = self.db.get_categories()
        self.parser = reqparse.RequestParser()

    def get(self, category_id=None):
        token = request.headers.get('Authorization')
        if not token:
            return { 'message': 'Unauthorized acces token not found'}, 401
        if not is_valid_token(token):
           return { 'message': 'Unauthorized invalid token'}, 401

        if category_id is not None:
            category = next((p for p in self.categories_data if p['id'] == category_id), None)
            if category is not None:
                return category
            else:
                return {'message': 'Category not found'}, 404
         
        return self.categories_data 

    def post(self):
        token = request.headers.get('Authorization')
        if not token:
            return { 'message': 'Unauthorized acces token not found'}, 401
        if not is_valid_token(token):
            return { 'message': 'Unauthorized invalid token'}, 401

        self.parser.add_argument('name', type=str, required=True, help='Name of the category')

        args = self.parser.parse_args()
        print("*****",args)
        new_category_name = args['name']
        if not new_category_name:
            return {'message': 'Category name is required'}, 400

        categories = self.categories_data
        if new_category_name in categories:
            return {'message': 'Category already exists'}, 400

        new_category = {
                'id': len(self.categories_data) + 1,
                'name': new_category_name
        }

        categories.append(new_category)
        self.categories_data = categories
        
        self.db.add_category(new_category)

        return {'message': 'Category added successfully'}, 201

    def delete(self):
        token = request.headers.get('Authorization')
        if not token:
            return { 'message': 'Unauthorized acces token not found'}, 401
        if not is_valid_token(token):
           return { 'message': 'Unauthorized invalid token'}, 401

        args = self.parser.parse_args()
        self.parser.add_argument('name', type=str, required=True, help='Name of the category')
        args = self.parser.parse_args()
        category_name = args['name']
 
        if not category_name:
            return {'message': 'Category name is required'}, 400

        category_to_remove = next((cat for cat in self.categories_data if cat["name"] == category_name), None)

        if category_to_remove is None:
            return {'message': 'Category not found'}, 404
        else:
            categories = [cat for cat in self.categories_data if cat["name"] != category_to_remove]
            self.categories_data = categories
            self.db.remove_category(category_name)

            return {'message': 'Category removed successfully'}, 200

