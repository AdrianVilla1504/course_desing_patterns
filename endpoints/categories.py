from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import json
from utils.database_connection import DatabaseConnection
from utils.authenticator import Authenticator

# Clase que gestiona las categorías.
# Aplica el patrón de diseño **Single Responsibility Principle (SRP)**,
# ya que esta clase tiene la única responsabilidad de manejar la lógica de categorías.
class CategoryManager:
    def __init__(self, db_connection):
        self.db = db_connection  # Se inyecta la conexión a la base de datos.
        self.categories_data = self.db.get_categories()  # Carga las categorías desde la base de datos.

    def add_category(self, name):
        # Verifica si la categoría ya existe.
        if name in [cat['name'] for cat in self.categories_data]:
            return {'message': 'Category already exists'}, 400

        # Crea una nueva categoría.
        new_category = {
            'id': len(self.categories_data) + 1,
            'name': name
        }

        # Agrega la nueva categoría a la lista y a la base de datos.
        self.categories_data.append(new_category)
        self.db.add_category(new_category)
        return {'message': 'Category added successfully'}, 201

    def remove_category(self, name):
        # Busca la categoría a eliminar.
        category_to_remove = next((cat for cat in self.categories_data if cat["name"] == name), None)

        # Verifica si la categoría no fue encontrada.
        if category_to_remove is None:
            return {'message': 'Category not found'}, 404

        # Elimina la categoría de la lista y de la base de datos.
        self.categories_data = [cat for cat in self.categories_data if cat["name"] != name]
        self.db.remove_category(name)
        return {'message': 'Category removed successfully'}, 200


# Clase que maneja las solicitudes HTTP relacionadas con las categorías.
# Aplica el patrón de diseño **Facade Pattern**,
# ya que simplifica la interacción con la lógica de negocio a través de CategoryManager.
class CategoriesResource(Resource):
    def __init__(self):
        self.db = DatabaseConnection('db.json')  # Crea una conexión a la base de datos.
        self.db.connect()  # Conecta a la base de datos.
        self.category_manager = CategoryManager(self.db)  # Crea un gestor de categorías.
        self.parser = reqparse.RequestParser()  # Inicializa el parser para los argumentos de la solicitud.
        self.parser.add_argument('name', type=str, required=True, help='Name of the category')  # Define el argumento 'name'.

    def get(self, category_id=None):
        # Aplica el patrón de diseño **Decorator Pattern** para la autenticación.
        # Verifica si el usuario está autenticado antes de procesar la solicitud.
        auth_response = Authenticator.authenticate()
        if auth_response:
            return auth_response

        # Si se proporciona un ID de categoría, busca la categoría específica.
        if category_id is not None:
            category = next((p for p in self.category_manager.categories_data if p['id'] == category_id), None)
            if category is not None:
                return category  # Retorna la categoría encontrada.
            else:
                return {'message': 'Category not found'}, 404  # Retorna un error si no se encuentra la categoría.

        # Si no se proporciona un ID, retorna todas las categorías.
        return self.category_manager.categories_data 

    def post(self):
        # Verifica la autenticación antes de procesar la solicitud.
        auth_response = Authenticator.authenticate()
        if auth_response:
            return auth_response

        # Parsea los argumentos de la solicitud y agrega una nueva categoría.
        args = self.parser.parse_args()
        return self.category_manager.add_category(args['name'])

    def delete(self):
        # Verifica la autenticación antes de procesar la solicitud.
        auth_response = Authenticator.authenticate()
        if auth_response:
            return auth_response

        # Parsea los argumentos de la solicitud y elimina una categoría.
        args = self.parser.parse_args()
        return self.category_manager.remove_category(args['name'])