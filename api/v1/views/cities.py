#!/usr/bin/python3
"""state pages"""
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State
from flask import abort, request, jsonify


@app_views.route("/states/<state_id>/cities",
                 strict_slashes=False,
                 methods=["GET"])
def cities_by_state(state_id):
    """get cities by state id"""
    cities_list = []
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    for city in state.cities:
        cities_list.append(city.to_dict())
    return jsonify(cities_list)


@app_views.route("/cities/<city_id>", strict_slashes=False, methods=["GET"])
def cities_get(city_id):
    """ get all cities with id"""
    city_by_id = storage.get(City, city_id)
    if city_by_id is None:
        abort(404)
    return jsonify(city_by_id.to_dict())


@app_views.route("/cities/<city_id>", strict_slashes=False,
                 methods=["DELETE"])
def delete_cities_id(city_id):
    """delete city by id"""
    city_by_id = storage.get(City, city_id)
    if city_by_id is None:
        abort(404)
    storage.delete(city_id)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states/<state_id>/cities",
                 methods=["POST"], strict_slashes=False)
def create_city(state_id):
    """create a new city"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    data = request.get_json(silent=True, force=True)
    if not data:
        abort(400, "Not a JSON")
    if "name" not in data:
        abort(400, "Missing name")
    state = City(state_id=state.id, **data)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route("/cities/<city_id>", strict_slashes=False,
                 methods=["PUT"])
def update_city(city_id):
    city_by_id = storage.get(City, city_id)
    if city_by_id is None:
        abort(404)
    data = request.get_json(silent=True, force=True)
    if not data:
        abort(400, "Not a JSON")
    city_by_id.name = data.get("name", city_by_id.name)
    city_by_id.save()
    return jsonify(city_by_id.to_dict()), 200
