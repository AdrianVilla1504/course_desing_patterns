from flask import Flask, request

# Función que valida el token de acceso.
# Este método es simple y no se asocia a un patrón de diseño específico.
def is_valid_token(token):
    return token == 'abcd1234'

# Clase Authenticator que se encarga de la autenticación.
# Aplica el **Principio de Responsabilidad Única (SRP)**,
# ya que esta clase tiene la única responsabilidad de manejar la autenticación.
class Authenticator:
    @staticmethod
    def authenticate():
        # Obtiene el token de la cabecera de la solicitud.
        token = request.headers.get('Authorization')
        
        # Verifica si el token no está presente.
        if not token:
            # Retorna un mensaje de error y un código de estado 401 (no autorizado).
            return {'message': 'Token de acceso no autorizado no encontrado'}, 401
        
        # Verifica si el token es válido.
        if not is_valid_token(token):
            # Retorna un mensaje de error y un código de estado 401 (no autorizado).
            return {'message': 'Token no autorizado inválido'}, 401
        
        # Si el token es válido, retorna None, indicando que la autenticación fue exitosa.
        return None