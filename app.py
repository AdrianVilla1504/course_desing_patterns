from flask import Flask
from flask_restful import Api
from utils.common import build_swagger_config_json
from endpoints.products import ProductsResource
from endpoints.auth import AuthenticationResource
from endpoints.categories import CategoriesResource
from endpoints.favorites import FavoritesResource
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
from endpoints.SwaggerConfig import SwaggerConfig 


import json

app = Flask(__name__)
api = Api(app)
CORS(app, resources={r"/*": {"origins": "*"}})
# ============================================
# Swagger
# ============================================
build_swagger_config_json()
swaggerui_blueprint = get_swaggerui_blueprint(
    "",
    f'http://localhost:5000/api/docs/',
    config={
        'app_name': "Flask API",
        "layout": "BaseLayout",
        "docExpansion": "none"
    },
)
app.register_blueprint(swaggerui_blueprint)

with open('db.json', 'r') as file:
    products = json.load(file)

api.add_resource(SwaggerConfig, '/api/docs/')

api.add_resource( AuthenticationResource,'/auth')

api.add_resource(ProductsResource, '/products', '/products/<int:product_id>') 

api.add_resource(CategoriesResource, '/categories', '/categories/<int:category_id>')

api.add_resource(FavoritesResource, '/favorites')

if __name__ == '__main__':
    app.run(debug=True)

