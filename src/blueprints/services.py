from flask import Blueprint, request, jsonify
from src.commands.ping import Ping
from src.commands.chatbot import GetNode
from src.errors.errors import BadRequest, NotFound

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
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@services_bp.route('/ping', methods=['GET'])
def ping():
    command = Ping()
    return jsonify({'message': command.execute()}), 200