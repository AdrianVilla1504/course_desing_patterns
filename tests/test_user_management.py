import unittest
from unittest.mock import MagicMock
from flask import Flask
from flask_restful import Api, reqparse  
from endpoints.users import UserManagementResource


class MockedUserManagementResource(UserManagementResource):
    """Subclase para inyectar un mock en lugar de la base de datos."""
    def __init__(self, mock_db):
        self.db = mock_db
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str, required=True, help='Username is required')
        self.parser.add_argument('role', type=str, required=False, help='Role is optional')



class TestUserManagementResource(unittest.TestCase):
    def setUp(self):
        """Configura el entorno de pruebas, incluyendo mocks."""
        self.app = Flask(__name__)
        self.api = Api(self.app)

        # Mock para DatabaseConnection
        self.mock_db = MagicMock()
        self.mock_db.get_items.return_value = []
        self.mock_db.add_item = MagicMock()
        self.mock_db._save_data = MagicMock()

        # Registrar el recurso usando la subclase con mock
        self.api.add_resource(
            MockedUserManagementResource,
            "/users",
            "/users/<string:username>",
            resource_class_args=(self.mock_db,)  # Argumentos para la inicialización
        )

        self.client = self.app.test_client()

    def test_get_all_users_success(self):
        """Prueba obtener todos los usuarios autenticados exitosamente."""
        self.mock_db.get_items.return_value = [
            {"username": "alice", "role": "admin"},
            {"username": "bob", "role": "viewer"}
        ]
        response = self.client.get("/users", headers={"Authorization": "abcd1234"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [
            {"username": "alice", "role": "admin"},
            {"username": "bob", "role": "viewer"}
        ])

    def test_post_new_user_success(self):
        """Prueba agregar un nuevo usuario exitosamente."""
        response = self.client.post(
            "/users",
            headers={"Authorization": "abcd1234"},
            json={"username": "charlie", "role": "editor"}
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {
            'message': 'User authenticated successfully',
            'user': {'username': "charlie", "role": "editor"}
        })
        self.mock_db.add_item.assert_called_with(
            "authenticated_users", {"username": "charlie", "role": "editor"}
        )

    def test_post_duplicate_user(self):
        """Prueba el caso donde se intenta agregar un usuario duplicado."""
        self.mock_db.get_items.return_value = [{"username": "alice", "role": "admin"}]
        response = self.client.post(
            "/users",
            headers={"Authorization": "abcd1234"},
            json={"username": "alice", "role": "admin"}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {'message': 'User already authenticated'})

    def test_delete_user_success(self):
        """Prueba eliminar un usuario exitosamente."""
        self.mock_db.get_items.return_value = [{"username": "alice", "role": "admin"}]
        response = self.client.delete(
            "/users",
            headers={"Authorization": "abcd1234"},
            json={"username": "alice"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'message': 'User removed successfully'})
        self.mock_db._save_data.assert_called_once()

    def test_delete_user_not_found(self):
        """Prueba el caso donde se intenta eliminar un usuario inexistente."""
        self.mock_db.get_items.return_value = []
        response = self.client.delete(
            "/users",
            headers={"Authorization": "abcd1234"},
            json={"username": "nonexistent_user"}
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {'message': 'User not found'})


if __name__ == "__main__":
    unittest.main()
