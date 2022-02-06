#!/usr/bin/python3
""" Starts a flask api"""

from api.v1.views import app_views
from flask import Flask, make_response, jsonify
from flask_cors import CORS
from models import storage
import os


app = Flask(__name__)
CORS(app, resources={"/api/*": {"origins": "0.0.0.0"}})
app.url_map.strict_slashes = False
CORS(app, resources={"/api/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def tear_down(self):
    """ removes the current SQLAlchemy session"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    if os.getenv("HBNB_API_HOST") and os.getenv("HBNB_API_PORT"):
        app.run(host=os.getenv("HBNB_API_HOST"),
                port=os.getenv("HBNB_API_PORT"), threaded=True)
    else:
        app.run(host='0.0.0.0', port=5000, threaded=True)
