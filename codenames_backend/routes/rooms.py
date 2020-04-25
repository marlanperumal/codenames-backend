from flask import request, jsonify, Blueprint, abort
from ..models import db
from ..models.rooms import Room, rooms_schema, room_schema

api = Blueprint("rooms", __name__)


@api.route("", methods=["GET"])
def get_rooms():
    rooms = Room.query.all()
    return rooms_schema.jsonify(rooms)


@api.route("/<string:id>", methods=["GET"])
def get_room(id):
    room = Room.query.get(id)
    if not room:
        abort(404, description="Room Code does not exist")
    return room_schema.jsonify(room)


@api.route("", methods=["POST"])
def new_room():
    room = Room()
    db.session.add(room)
    db.session.commit()
    return room_schema.jsonify(room), 201


@api.route("/<string:id>", methods=["PATCH", "PUT"])
def update_room(id):
    room = Room.query.get(id)
    data = request.get_json()
    room_data = room_schema.load(data)
    for key, value in room_data.items():
        setattr(room, key, value)
    db.session.commit()
    return room_schema.jsonify(room)


@api.route("/<string:id>", methods=["DELETE"])
def delete_room(id):
    room = Room.query.get(id)
    db.session.delete(room)
    db.session.commit()
    return jsonify(""), 204
