from flask import Blueprint, request
from flask_restful import Resource, Api

class AuthenticationResource(Resource):
    def post(self):
        username = request.json.get('username')
        password = request.json.get('password')

        if username == 'student' and password == 'desingp':
            token = 'abcd12345'
            return {'token': token}, 200
        else:
            return {'message': 'unauthorized'}, 401



