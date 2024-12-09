from flask_restful import Resource, reqparse
from flask import request
from utils.database_connection import DatabaseConnection

def is_valid_token(token):
    return token == 'abcd1234'


class FavoritesResource(Resource):
    def __init__(self):
        # Aplicación del patrón Singleton para mantener una única conexión con la base de datos
        self.db = DatabaseConnection('favorites.json')
        self.db.connect()

        # Uso del patrón Builder para configurar el parser de argumentos
        self.parser = self._build_parser()

    def _build_parser(self):
        """
        Construye y retorna el parser de argumentos.
        Patrón: Builder
        """
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=int, required=True, help='User ID is required')
        parser.add_argument('product_id', type=int, required=True, help='Product ID is required')
        return parser

    def _authenticate(self):
        """
        Verifica la autenticación del token.
        Patrón: Template Method (reutilización de lógica común).
        """
        token = request.headers.get('Authorization')

        if not token:
            return {'message': 'Unauthorized: access token not found'}, 401

        if not is_valid_token(token):
            return {'message': 'Unauthorized: invalid token'}, 401

        return None

    def get(self):
        """
        Devuelve todos los productos favoritos.
        """
        # Aplicamos el patrón Template Method con _authenticate
        auth_error = self._authenticate()
        if auth_error:
            return auth_error

        try:
            return self.db.get_favorites(), 200
        except Exception as e:
            return {'message': f'Error retrieving favorites: {str(e)}'}, 500

    def post(self):
        """
        Agrega un nuevo producto a los favoritos.
        """
        # Patrón Template Method con _authenticate
        auth_error = self._authenticate()
        if auth_error:
            return auth_error

        args = self.parser.parse_args()
        favorites = self.db.get_favorites()

        # Patrón Command: encapsular lógica para verificar favoritos existentes
        if self._is_favorite_exist(args['user_id'], args['product_id'], favorites):
            return {'message': 'Product already in favorites'}, 400

        # Crear el nuevo favorito y agregarlo (Simple Factory para crear favoritos)
        new_favorite = self._create_favorite(args['user_id'], args['product_id'])
        self.db.add_favorite(new_favorite)

        return {'message': 'Product added to favorites', 'favorite': new_favorite}, 201

    def delete(self):
        """
        Elimina un producto de los favoritos.
        """
        # Patrón Template Method con _authenticate
        auth_error = self._authenticate()
        if auth_error:
            return auth_error

        args = self.parser.parse_args()
        favorites = self.db.get_favorites()

        # Patrón Command: buscar y eliminar favorito
        favorite_to_remove = self._find_favorite(args['user_id'], args['product_id'], favorites)
        if not favorite_to_remove:
            return {'message': 'Favorite not found'}, 404

        self._remove_favorite(favorite_to_remove, favorites)

        return {'message': 'Product removed from favorites'}, 200

    def _is_favorite_exist(self, user_id, product_id, favorites):
        """
        Verifica si un producto ya está en favoritos.
        Patrón: Command (encapsular la lógica).
        """
        return any(fav['user_id'] == user_id and fav['product_id'] == product_id for fav in favorites)

    def _create_favorite(self, user_id, product_id):
        """
        Crea un nuevo favorito.
        Patrón: Simple Factory
        """
        return {
            'user_id': user_id,
            'product_id': product_id
        }

    def _find_favorite(self, user_id, product_id, favorites):
        """
        Encuentra un favorito específico.
        Patrón: Command
        """
        return next(
            (fav for fav in favorites if fav['user_id'] == user_id and fav['product_id'] == product_id),
            None
        )

    def _remove_favorite(self, favorite, favorites):
        """
        Elimina un favorito de la lista.
        Patrón: Command
        """
        self.db.data['favorites'] = [
            fav for fav in favorites if fav != favorite
        ]
        self.db._save_data()
