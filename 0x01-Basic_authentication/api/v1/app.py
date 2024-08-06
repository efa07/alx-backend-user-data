#!/usr/bin/env python3
"""
Route module for the API
"""
from api.v1.views import app_views
from api.v1.auth.auth import Auth
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os
import importlib


auth = None

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

auth_type = getenv("AUTH_TYPE")
if auth_type:
    try:
        auth_module = importlib.import_module(f"api.v1.auth.{auth_type.lower()}")
        auth_class = getattr(auth_module, auth_type)
        auth = auth_class()
    except (ImportError, AttributeError) as e:
        print(f"Error loading authentication class: {e}")

@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """ Unauthorized handler """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """Forbidden handler"""
    return jsonify({"error": "Forbidden"}), 403


@app.before_request
def before_request():
    """
    Method to filter requests based on authentication requirements.
    """
    if auth is None:
        return

    excluded_paths = ['/api/v1/status/', '/api/v1/unauthorized/',
                      '/api/v1/forbidden/']

    if request.path not in excluded_paths:
        if auth.require_auth(request.path, excluded_paths):
            if auth.authorization_header(request) is None:
                abort(401)
            if auth.current_user(request) is None:
                abort(403)


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
