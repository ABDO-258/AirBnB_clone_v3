#!/usr/bin/python3
"""amenities pages"""
from api.v1.views import app_views
from models import storage
from models.users import User
from flask import abort, request, jsonify


@app_views.route("/users", methods=["GET"], strict_slashes=False)
@app_views.route("users/<user_id>", strict_slashes=False,
                 methods=["GET"])
def users_get(user_id=None):
    """ get all users or user with id"""
    user_list = []
    if user_id is None:
        users_obj = storage.all("User")
        for user in users_obj.values():
            user_list.append(user.to_dict())
        return jsonify(user_list)
    else:
        user_by_id = storage.get(User, user_id)
        if user_by_id is None:
            abort(404)
        return jsonify(user_by_id.to_dict())


@app_views.route("/users/<user_id>", strict_slashes=False,
                 methods=["DELETE"])
def delete_user_id(amenity_id):
    """delete user by id"""
    user_by_id = storage.get(User, user_id)
    if user_by_id is None:
        abort(404)
    storage.delete(user_by_id)
    storage.save()
    return jsonify({}), 200


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def create_user():
    """create a new user"""
    data = request.get_json(silent=True, force=True)
    if not data:
        abort(400, "Not a JSON")
    if "email" not in data:
        abort(400, "Missing email")
    if "password" not in data:
        abort(400, "Missing password")
    user = User(**data)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route("/users/<user_id>", strict_slashes=False,
                 methods=["PUT"])
def update_user(user_id):
    """ update a user"""
    user_by_id = storage.get(User, user_id)
    if user_by_id is None:
        abort(404)
    data = request.get_json(silent=True, force=True)
    if not data:
        abort(400, "Not a JSON")
    user_by_id.password = data.get("password", user_by_id.password)
    user_by_id.first_name = data.get("first_name", user_by_id.first_name)
    user_by_id.last_name = data.get("last_name", user_by_id.last_name)
    user_by_id.save()
    return jsonify(user_by_id.to_dict()), 200
