#!/usr/bin/python3
"""state pages"""
from api.v1.views import app_views
from models import storage
from models.state import State
from flask import abort, request, jsonify


@app_views.route("/states", methods=["GET"], strict_slashes=False)
@app_views.route("/states/<state_id>", strict_slashes=False, methods=["GET"])
def states_get(state_id=None):
    """ get all states or with id"""
    states_list = []
    if state_id is None:
        states_obj = storage.all("State")
        for state_obj in states_obj.values():
            states_list.append(state_obj.to_dict())
        return jsonify(states_list)
    else:
        state_by_id = storage.get(State,state_id)
        if state_by_id is None:
            abort(404)
        return jsonify(state_by_id.to_dict())

@app_views.route("/states/<state_id>", strict_slashes=False,
                 methods=["DELETE"])
def delete_state_id(state_id):
    """delete state by id"""
    state__id = storage.get(State, state_id)
    if state__id is None:
        abort(404)
    storage.delete(state__id)
    storage.save()
    return jsonify({}), 200

@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create():
    """create a new state"""
    data = request.get_json(silent=True, force=True)
    if not data:
        abort(400, "Not a JSON")
    if "name"  not in data:
        abort(400, "Missing name")
    state = State(**data)
    state.save()
    return jsonify(state.to_dict()), 201

@app_views.route("/states/<state_id>", strict_slashes=False,
                 methods=["PUT"])
def update_state(state_id):
    state__id = storage.get(State, state_id)
    if state__id is None:
        abort(404)
    data = request.get_json(silent=True, force=True)
    if not data:
        abort(400, "Not a JSON")
    state__id.name = data.get("name", state__id.name)
    state__id.save()
    return jsonify(state__id.to_dict()), 200
