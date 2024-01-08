#!/usr/bin/python3
"""places pages"""
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from flask import abort, request, jsonify


@app_views.route("/cities/<city_id>/places", strict_slashes=False,
                 methods=["GET"])
def places_get(city_id=None):
    """ get all places  in a city with id"""
    places_list = []
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = city.places
    for place in places:
        places_list.append(place.to_dict())
    return jsonify(places_list)


@app_views.route("/places/<place_id>", methods=["GET"], strict_slashes=False)
def place_by_id(place_id):
    """get all places with id"""
    places = storage.get(Place, place_id)
    if places is None:
        abort(404)
    return jsonify(places.to_dict)


@app_views.route("/places/<place_id>", strict_slashes=False,
                 methods=["DELETE"])
def delete_place_id(place_id):
    """delete state by id"""
    Place_by_id = storage.get(Place, place_id)
    if place_by_id is None:
        abort(404)
    storage.delete(place_by_id)
    storage.save()
    return jsonify({}), 200


@app_views.route("/cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
def create_place(city_id):
    """create a new place"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data = request.get_json(silent=True, force=True)
    if not data:
        abort(400, "Not a JSON")
    if "user_id" not in data:
        abort(400, "Missing user_id")
    user = storage.get(User, data["user_id"])
    if user is None:
        abort(404)
    if "name" not in data:
        abort(400, "Missing name")
    place = Place(city_id=city.id, **data)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route("/places/<place_id>", strict_slashes=False,
                 methods=["PUT"])
def update_place(place_id):
    place_by_id = storage.get(Place, place_id)
    if place_by_id is None:
        abort(404)
    data = request.get_json(silent=True, force=True)
    if not data:
        abort(400, "Not a JSON")
    place_by_id.name = data.get("name", place_by_id.name)
    place_by_id.description = data.get("description", place_by_id.description)
    place_by_id.number_rooms = data.get("number_rooms",
                                        place_by_id.number_rooms)
    place_by_id.number_bathrooms = data.get("number_bathrooms",
                                            place_by_id.number_bathrooms)
    place_by_id.max_guest = data.get("max_guest", place_by_id.max_guest)
    place_by_id.price_by_night = data.get("price_by_night",
                                          place_by_id.price_by_night)
    place_by_id.latitude = data.get("latitude", place_by_id.latitude)
    place_by_id.longitude = data.get("longitude", place_by_id.longitude)

    place_by_id.save()
    return jsonify(place_by_id.to_dict()), 200
