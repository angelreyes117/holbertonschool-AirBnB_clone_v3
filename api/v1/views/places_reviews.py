#!/usr/bin/python3
"""Reviews RESTful API"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<string:place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def get_reviews(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify([review.to_dict() for review in place.reviews])


@app_views.route('/reviews/<string:review_id>',
                 methods=['GET'], strict_slashes=False)
def get_review(review_id):
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<string:review_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<string:place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def create_review(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = request.get_json(silent=True)
    if data is None:
        return make_response(jsonify(error="Not a JSON"), 400)
    if 'user_id' not in data:
        return make_response(jsonify(error="Missing user_id"), 400)
    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404)
    if 'text' not in data:
        return make_response(jsonify(error="Missing text"), 400)
    data['place_id'] = place_id
    review = Review(**data)
    storage.new(review)
    storage.save()
    return make_response(jsonify(review.to_dict()), 201)


@app_views.route('/reviews/<string:review_id>',
                 methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    data = request.get_json(silent=True)
    if data is None:
        return make_response(jsonify(error="Not a JSON"), 400)
    ignore = ('id', 'user_id', 'place_id', 'created_at', 'updated_at')
    for key, value in data.items():
        if key not in ignore:
            setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict()), 200
