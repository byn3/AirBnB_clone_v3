#!/usr/bin/python3
"""Endpint that returns the status of the API"""
from models import storage
from flask import Flask, render_template, jsonify, Blueprint
from api.v1.views import app_views
from os import getenv, environ
app = Flask(__name__)
app.register_blueprint(app_views)
app.config.update(JSONIFY_PRETTYPRINT_REGULAR=True)


@app.errorhandler(404)
def not_found(e):
    """ Gives the 404 not found page """
    return (jsonify({"error": "Not found"}), 404)

"""
def create_app(config_filename):
    "" Helps aid in making a 404 page ""
    app.register_error_handler(404, page_not_found)
    return app
"""


@app.teardown_appcontext
def teardown(error):
    """ tears down and saves the storage """
    storage.close()

if __name__ == '__main__':
    port = '5000'
    host = '0.0.0.0'
    if environ.get('HBNB_API_HOST'):
        host = getenv('HBNB_API_HOST')
    if environ.get('HBNB_API_PORT'):
        port = getenv('HBNB_API_PORT')
    app.run(host=host, port=int(port), threaded=True)
