import os
import requests
from flask import Flask, request, jsonify
from db_users import createuser, getusers, finduser

app = Flask(__name__)

# Cargar el nombre del binding de Dapr desde las variables de entorno o usar un valor por defecto
DB_BINDING_NAME = os.getenv('DB_BINDING_NAME', 'my-mysql')

# Base URL de Dapr
DAPR_BASE_URL = f"http://localhost:3500/v1.0/bindings/{DB_BINDING_NAME}"

def call_dapr_service(body):
    """
    Realiza la llamada al servicio de Dapr para ejecutar la operación en MySQL.
    Si hay un error en la llamada, captura y maneja la excepción.
    """
    try:
        response = requests.post(DAPR_BASE_URL, json=body)
        response.raise_for_status()  # Lanza un error para cualquier código de estado HTTP 4xx o 5xx
        return response
    except requests.exceptions.RequestException as e:
        # Loggear el error adecuadamente (puedes usar una librería como logging)
        print(f"Error en la comunicación con Dapr: {e}")
        return None


@app.route('/users', methods=['GET'])
def get_all_users():
    """
    Ruta para obtener todos los usuarios.
    Llama al servicio de Dapr para ejecutar la consulta en MySQL.
    """
    body = getusers()  # Genera el cuerpo de la consulta SQL para obtener todos los usuarios
    response = call_dapr_service(body)

    if not response:
        return jsonify({"status": "error", "message": "Error en la comunicación con Dapr"}), 500

    return jsonify({"status": "success", "data": response.json()}), 200


@app.route('/users/<username>', methods=['GET'])
def get_user(username):
    """
    Ruta para obtener un usuario específico por su nombre de usuario.
    Si el usuario no existe, devuelve un error.
    """
    body = finduser(username)  # Genera el cuerpo de la consulta SQL para buscar al usuario por nombre
    response = call_dapr_service(body)

    if not response:
        return jsonify({"status": "error", "message": "Error en la comunicación con Dapr"}), 500

    data = response.json()
    if not data:
        return jsonify({"status": "error", "message": "Usuario no encontrado"}), 404

    return jsonify({"status": "success", "data": data}), 200


@app.route('/users', methods=['POST'])
def create_new_user():
    """
    Ruta para crear un nuevo usuario.
    Primero verifica si el usuario ya existe; si es así, devuelve un error.
    Si no existe, lo crea en la base de datos.
    """
    user_data = request.json
    username = user_data.get("username")
    email = user_data.get("email")

    if not username or not email:
        return jsonify({"status": "error", "message": "Faltan campos requeridos: username y email"}), 400

    # Verificar si el usuario ya existe
    body = finduser(username)
    response = call_dapr_service(body)

    if not response:
        return jsonify({"status": "error", "message": "Error en la comunicación con Dapr"}), 500

    if response.json():  # Si el usuario ya existe
        return jsonify({"status": "error", "message": "El usuario ya existe"}), 400

    # Crear el nuevo usuario
    body = createuser(username, email)
    create_response = call_dapr_service(body)

    if not create_response:
        return jsonify({"status": "error", "message": "Error en la creación del usuario"}), 500

    return jsonify({"status": "success", "message": "Usuario creado con éxito"}), 201


if __name__ == '__main__':
    app.run(port=5000)
