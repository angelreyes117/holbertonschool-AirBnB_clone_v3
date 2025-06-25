#!/usr/bin/python3
"""View of Rlaces Reviews for RESTFul API"""

from api.v1.views import app_views, validate_model, get_json
from flask import jsonify, abort, request
from models import storage, class_dictionary


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    """Get all reviews of a place"""
    place = validate_model("Place", place_id)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """Get a review"""
    review = validate_model("Review", review_id)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Delete a review"""
    review = validate_model("Review", review_id)
    review.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    """POST scenario - new review of place id supplied"""
    place = validate_model("Place", place_id)
    if place is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    user_id = data.get('user_id')
    if user_id is None:
        abort(400)
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    text = data.get('text')
    if text is None:
        abort(400, 'Missing text')
    review = storage.class_dictionary["Review"](place_id=place_id,
                                                user_id=user_id, text=text)
    review.save()
    storage.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """PUT scenario - updated review of place_id"""
    review = validate_model("Review", review_id)
    data = get_json()
    for key, value in data.items():
        if key not in ['id', 'user_id',
                       'place_id', 'created_at', 'updated_at']:
            setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict()), 200
