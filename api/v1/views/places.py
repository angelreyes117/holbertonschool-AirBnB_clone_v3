#!/usr/bin/python3
"""Places RESTful API"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.city import City
from models.user import User
from models.place import Place


@app_views.route('/cities/<string:city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_places(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify([place.to_dict() for place in city.places])


@app_views.route('/places/<string:place_id>',
                 methods=['GET'], strict_slashes=False)
def get_place(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<string:place_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<string:city_id>/places',
                 methods=['POST'], strict_slashes=False)
def create_place(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data = request.get_json(silent=True)
    if data is None:
        return make_response(jsonify(error="Not a JSON"), 400)
    if 'user_id' not in data:
        return make_response(jsonify(error="Missing user_id"), 400)
    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404)
    if 'name' not in data:
        return make_response(jsonify(error="Missing name"), 400)
    data['city_id'] = city_id
    place = Place(**data)
    storage.new(place)
    storage.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<string:place_id>',
                 methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = request.get_json(silent=True)
    if data is None:
        return make_response(jsonify(error="Not a JSON"), 400)
    ignore = ('id', 'user_id', 'city_id', 'created_at', 'updated_at')
    for key, value in data.items():
        if key not in ignore:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200
