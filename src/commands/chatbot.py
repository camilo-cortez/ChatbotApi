from flask import jsonify
from commands.base_command import BaseCommand
from decision_tree import get_tree_node
from errors.errors import BadRequest

class GetNode(BaseCommand):
    def __init__(self, json):
        self.path = json.get('path', '').strip()
        self.id = json.get('id', '').strip()
        # self.id_number = json.get('idNumber', '').strip()
        # self.phone_number = json.get('phoneNumber', '').strip()
        # self.plan = json.get('plan', Plan.EMPRESARIO)

    def execute(self):
        try:
            node = get_tree_node(self.path)
            return jsonify(node)

            if not (self.name and self.password and self.email):
                raise BadRequest('Name, password, and email are required')

            valid_email = validators.email(self.email)
            if not valid_email:
                raise BadRequest('Invalid email format')

           

        except Exception as e:
            raise e
