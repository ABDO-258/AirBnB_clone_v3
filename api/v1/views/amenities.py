#!/usr/bin/python3
"""amenities pages"""
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from flask import abort, request, jsonify


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
@app_views.route("amenities/<amenity_id>", strict_slashes=False,
                 methods=["GET"])
def amenities_get(amenity_id=None):
    """ get all amenity or amenity with id"""
    amenity_list = []
    if amenity_id is None:
        amenities_obj = storage.all("Amenity")
        for amenity in amenities_obj.values():
            amenity_list.append(amenity.to_dict())
        return jsonify(amenity_list)
    else:
        amenity_by_id = storage.get(Amenity, amenity_id)
        if amenity_by_id is None:
            abort(404)
        return jsonify(amenity_by_id.to_dict())


@app_views.route("/amenities/<amenity_id>", strict_slashes=False,
                 methods=["DELETE"])
def delete_amenity_id(amenity_id):
    """delete state by id"""
    amenity_by_id = storage.get(Amenity, amenity_id)
    if amenity_by_id is None:
        abort(404)
    storage.delete(amenity_by_id)
    storage.save()
    return jsonify({}), 200


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def create_amenity():
    """create a new amenity"""
    data = request.get_json(silent=True, force=True)
    if not data:
        abort(400, "Not a JSON")
    if "name" not in data:
        abort(400, "Missing name")
    amenity = Amenity(**data)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", strict_slashes=False,
                 methods=["PUT"])
def update_amenity(amenity_id):
    amenity_by_id = storage.get(Amenity, amenity_id)
    if amenity_by_id is None:
        abort(404)
    data = request.get_json(silent=True, force=True)
    if not data:
        abort(400, "Not a JSON")
    amenity_by_id.name = data.get("name", amenity_by_id.name)
    amenity_by_id.save()
    return jsonify(amenity_by_id.to_dict()), 200
