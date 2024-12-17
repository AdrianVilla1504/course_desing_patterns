from flask_restful import Resource, reqparse
from flask import request
from utils.database_connection import DatabaseConnection
from utils.authenticator import Authenticator
from utils.filters import CategoryFilter, IDFilter

class ProductsResource(Resource):
    def __init__(self):
        self.db = DatabaseConnection('db.json')
        self.filters = {
            'category': CategoryFilter(),
            'id': IDFilter()
        }

    def get(self, product_id=None):
        # Validación de autenticación
        auth_error = Authenticator.authenticate()
        if auth_error:
            return auth_error

        # Filtrar por categoría
        category_filter = request.args.get('category')
        if category_filter:
            return self.filters['category'].filter(self.db.get_products(), category=category_filter)

        # Obtener producto por ID
        if product_id is not None:
            product = self.filters['id'].filter(self.db.get_products(), product_id=product_id)
            if product:
                return product
            return {'message': 'Product not found'}, 404

        # Devolver todos los productos
        return self.db.get_products()

    def post(self):
        # Validación de autenticación
        auth_error = Authenticator.authenticate()
        if auth_error:
            return auth_error

        # Parsear argumentos
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help='Name of the product')
        parser.add_argument('category', type=str, required=True, help='Category of the product')
        parser.add_argument('price', type=float, required=True, help='Price of the product')
        args = parser.parse_args()

        # Crear nuevo producto
        new_product = {
            'id': len(self.db.get_products()) + 1,
            'name': args['name'],
            'category': args['category'],
            'price': args['price']
        }

        self.db.add_product(new_product)
        return new_product, 201