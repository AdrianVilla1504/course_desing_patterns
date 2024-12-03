from flask import Flask
from flask_restful import Api
from endpoints.products import ProductsResource
from endpoints.auth import AuthenticationResource
from endpoints.categories import CategoriesResource
from endpoints.favorites import FavoritesResource

app = Flask(__name__)
api = Api(app)

import json
with open('db.json', 'r') as file:
    products = json.load(file)

api.add_resource( AuthenticationResource,'/auth')

api.add_resource(ProductsResource, '/products', '/products/<int:product_id>') 

api.add_resource(CategoriesResource, '/categories', '/categories/<int:category_id>')

api.add_resource(FavoritesResource, '/favorites')

if __name__ == '__main__':
    app.run(debug=True)

