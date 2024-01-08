#!/usr/bin/python3
"""places pages"""
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review
from models.user import User
from flask import abort, request, jsonify


@app_views.route("/places/<place_id>/reviews", strict_slashes=False,
                 methods=["GET"])
def reviews_get(place_id):
    """ Retrieves the list of all Review objects of a Place"""
    reviews_list = []
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = place.reviews
    for review in reviews:
        reviews_list.append(review.to_dict())
    return jsonify(reviews_list)


@app_views.route("/reviews/<review_id>", methods=["GET"],
                 strict_slashes=False)
def review_by_id(review_id):
    """get review_by_id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict)


@app_views.route("/reviews/<review_id>", strict_slashes=False,
                 methods=["DELETE"])
def delete_review_id(review_id):
    """delete state by id"""
    review_by_id = storage.get(Review, review_id)
    if review_by_id is None:
        abort(404)
    storage.delete(review_by_id)
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews", methods=["POST"],
                 strict_slashes=False)
def create_reviews(place_id):
    """create a new reviews"""
    place = storage.get(Place, place_id)
    if place_id is None:
        abort(404)
    data = request.get_json(silent=True, force=True)
    if not data:
        abort(400, "Not a JSON")
    if "user_id" not in data:
        abort(400, "Missing user_id")
    user = storage.get(User, data["user_id"])
    if user is None:
        abort(404)
    if "text" not in data:
        abort(400, "Missing text")
    review = Review(place_id=place.id, **data)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route("/reviews/<review_id>", strict_slashes=False,
                 methods=["PUT"])
def update_review(review_id):
    review_by_id = storage.get(Review, review_id)
    if review_by_id is None:
        abort(404)
    data = request.get_json(silent=True, force=True)
    if not data:
        abort(400, "Not a JSON")
    review_by_id.text = data.get("text", review_by_id.text)

    review_by_id.save()
    return jsonify(review_by_id.to_dict()), 200
