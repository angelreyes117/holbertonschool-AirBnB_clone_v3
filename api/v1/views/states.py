#!/usr/bin/python3
"""State Views RESTful API"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State

@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states_list():
    """Retrieve all State objects"""
    all_states = storage.all(State).values()
    return jsonify([state.to_dict() for state in all_states])

@app_views.route('/states/<string:state_id>', methods=['GET'], strict_slashes=False)
def state_get(state_id):
    """Retrieve a State by ID"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())

@app_views.route('/states/<string:state_id>', methods=['DELETE'], strict_slashes=False)
def state_delete(state_id):
    """Delete a State by ID"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200

@app_views.route('/states', methods=['POST'], strict_slashes=False)
def state_post():
    """Create a State"""
    data = request.get_json(silent=True)
    if data is None:
        return make_response(jsonify(error="Not a JSON"), 400)
    if 'name' not in data:
        return make_response(jsonify(error="Missing name"), 400)
    new_state = State(**data)
    storage.new(new_state)
    storage.save()
    return make_response(jsonify(new_state.to_dict()), 201)

@app_views.route('/states/<string:state_id>', methods=['PUT'], strict_slashes=False)
def state_put(state_id):
    """Update a State by ID"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    data = request.get_json(silent=True)
    if data is None:
        return make_response(jsonify(error="Not a JSON"), 400)
    for key, value in data.items():
        if key not in ('id', 'created_at', 'updated_at'):
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200
