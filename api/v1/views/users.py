#!/usr/bin/python3
"""Users RESTful API"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    return jsonify([u.to_dict() for u in storage.all(User).values()])


@app_views.route('/users/<string:user_id>',
                 methods=['GET'], strict_slashes=False)
def get_user(user_id):
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<string:user_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    data = request.get_json(silent=True)
    if data is None:
        return make_response(jsonify(error="Not a JSON"), 400)
    if 'email' not in data:
        return make_response(jsonify(error="Missing email"), 400)
    if 'password' not in data:
        return make_response(jsonify(error="Missing password"), 400)
    user = User(**data)
    storage.new(user)
    storage.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<string:user_id>',
                 methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    data = request.get_json(silent=True)
    if data is None:
        return make_response(jsonify(error="Not a JSON"), 400)
    ignore = ('id', 'email', 'created_at', 'updated_at')
    for key, value in data.items():
        if key not in ignore:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200
