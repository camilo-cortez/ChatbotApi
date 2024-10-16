from flask import Flask, jsonify, request
from decision_tree import get_tree_node
import os
import traceback
from flask import Flask, jsonify
from blueprints.services import services_bp

def create_app(config_name):
    app = Flask(config_name)
    app.register_blueprint(services_bp, url_prefix='/api')

    app_context = app.app_context()
    app_context.push()

    return app

app = create_app('chatbotapi')

@app.errorhandler(Exception)
def handle_exception(err):
    trace = traceback.format_exc()
    response = {
        "msg": getattr(err, 'description', str(err)),
        "traceback": trace
    }
    return jsonify(response), getattr(err, 'code', 500)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5008)
