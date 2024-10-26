from flask import jsonify
from src.commands.base_command import BaseCommand
from src.decision_tree import get_tree_node
from src.errors.errors import BadRequest, NotFound

class GetNode(BaseCommand):
    def __init__(self, json):
        self.path = json.get('path', '').strip()
        self.user_id = json.get('user_id', '').strip()
        self.incident_id = json.get('incident_id', '').strip()

    def execute(self):
        if self.path is None:
            raise BadRequest
        try:
            node = get_tree_node(self.path, self.user_id, self.incident_id)
            return jsonify(node)

        except Exception as e:
            raise NotFound
