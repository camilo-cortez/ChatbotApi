from flask import Blueprint, request, jsonify
from commands.ping import Ping
from commands.chatbot import GetNode
from errors.errors import BadRequest, NotFound

services_bp = Blueprint('services', __name__)

@services_bp.route('/getnode', methods=['GET'])
def create_client():
    try:
        json_input = request.get_json()
        command = GetNode(json_input)
        result = command.execute()
        return result, 201
    except BadRequest as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@services_bp.route('/ping', methods=['GET'])
def ping():
    command = Ping()
    return jsonify({'message': command.execute()}), 200