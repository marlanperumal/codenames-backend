from flask import request, jsonify, Blueprint
from ..models import db
from ..models.cards import Card, cards_schema, card_schema

api = Blueprint("cards", __name__)


@api.route("", methods=["GET"])
def get_cards():
    game_id = request.args.get("game_id")
    query = Card.query
    if game_id:
        query = query.filter_by(game_id=game_id)
    query = query.order_by("id")
    cards = query.all()
    return cards_schema.jsonify(cards)


@api.route("", methods=["POST"])
def add_card():
    data = request.get_json()
    card_data = card_schema.load(data)
    card = Card(**card_data)
    db.session.add(card)
    db.session.commit()
    return card_schema.jsonify(card), 201


@api.route("/<int:id>", methods=["PATCH", "PUT"])
def update_card(id):
    card = Card.query.get(id)
    data = request.get_json()
    card_data = card_schema.load(data)
    for key, value in card_data.items():
        setattr(card, key, value)
    db.session.commit()
    return card_schema.jsonify(card)


@api.route("/<int:id>", methods=["DELETE"])
def delete_card(id):
    card = Card.query.get(id)
    db.session.delete(card)
    db.session.commit()
    return jsonify(""), 204
