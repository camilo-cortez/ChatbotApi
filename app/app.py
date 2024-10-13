from flask import Flask, jsonify, request
from decision_tree import get_tree_node

app = Flask(__name__)

@app.route('/')
def hello():
	return "Hello World!"

@app.route('/api/getnode', methods=['GET'])
def get_data():
	data = request.json
	node = get_tree_node(data['path'])
	return jsonify(node)


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000)
