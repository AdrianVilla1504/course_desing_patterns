from flask_restful import Resource, reqparse
from flask import request
from utils.database_connection import DatabaseConnection

def is_valid_token(token):
    return token == 'abcd1234'

class UserManagementResource(Resource):
    """
    Recurso para gestionar usuarios autenticados en el sistema.
    Permite listar, agregar y eliminar usuarios autenticados.
    """

    def __init__(self):
        """
        Inicializa el recurso con una conexión a la base de datos y un analizador de argumentos (reqparse).

        Patrones utilizados:
        - **Repository**: Utiliza `DatabaseConnection` para abstraer y centralizar el acceso a los datos.
        - **Factory**: Facilita la creación de usuarios con roles consistentes.
        """
        self.db = DatabaseConnection('db.json')
        self.db.connect()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str, required=True, help='Username is required')
        self.parser.add_argument('role', type=str, required=False, help='Role is optional')

    def get(self, username=None):
        """
        Obtiene todos los usuarios autenticados o uno específico si se proporciona `username`.

        Patrones utilizados:
        - **Repository**: Los datos de usuarios autenticados se manejan a través de `DatabaseConnection`, lo que desacopla el acceso a datos de la lógica del negocio.
        """
        token = request.headers.get('Authorization')

        if not token:
            return {'message': 'Unauthorized access token not found'}, 401

        if not is_valid_token(token):
            return {'message': 'Unauthorized invalid token'}, 401

        authenticated_users = self.db.get_items('authenticated_users')

        if username:
            user = next((u for u in authenticated_users if u['username'] == username), None)
            if user:
                return user, 200
            return {'message': 'User not found'}, 404

        return authenticated_users, 200

    def post(self):
        """
        Autentica un nuevo usuario y lo guarda en el sistema.

        Patrones utilizados:
        - **Factory**: Crea un nuevo usuario con un formato consistente, asignando atributos como `username` y `role`.
        - **Repository**: Utiliza `DatabaseConnection` para gestionar los usuarios autenticados de manera centralizada.
        """
        token = request.headers.get('Authorization')

        if not token:
            return {'message': 'Unauthorized access token not found'}, 401

        if not is_valid_token(token):
            return {'message': 'Unauthorized invalid token'}, 401

        args = self.parser.parse_args()
        new_user = {
            'username': args['username'],
            'role': args.get('role', 'viewer')  # Rol por defecto: "viewer"
        }

        # Verifica si el usuario ya está autenticado
        existing_users = self.db.get_items('authenticated_users')
        if any(user['username'] == new_user['username'] for user in existing_users):
            return {'message': 'User already authenticated'}, 400

        # Agrega el nuevo usuario autenticado
        self.db._add_item('authenticated_users', new_user)
        return {'message': 'User authenticated successfully', 'user': new_user}, 201

    def delete(self):
        """
        Elimina un usuario autenticado del sistema.

        Patrones utilizados:
        - **Repository**: Accede a los datos y elimina usuarios de la lista gestionada por `DatabaseConnection`.
        """
        token = request.headers.get('Authorization')

        if not token:
            return {'message': 'Unauthorized access token not found'}, 401

        if not is_valid_token(token):
            return {'message': 'Unauthorized invalid token'}, 401

        args = self.parser.parse_args()
        username_to_remove = args['username']

        existing_users = self.db.get_items('authenticated_users')
        user_to_remove = next((u for u in existing_users if u['username'] == username_to_remove), None)

        if not user_to_remove:
            return {'message': 'User not found'}, 404

        # Filtra para eliminar el usuario
        updated_users = [u for u in existing_users if u['username'] != username_to_remove]
        self.db.data['authenticated_users'] = updated_users
        self.db._save_data()

        return {'message': 'User removed successfully'}, 200
