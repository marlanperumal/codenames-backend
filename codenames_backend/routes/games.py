from flask import request, jsonify, Blueprint
from ..models import db
from ..models.cards import Card, cards_schema
from ..models.games import Game, games_schema, game_schema

api = Blueprint("games", __name__)


@api.route("", methods=["GET"])
def get_games():
    games = Game.query.all()
    return games_schema.jsonify(games)


@api.route("/<string:id>/cards", methods=["GET"])
def get_game_cards(id):
    cards = Card.query.filter_by(game_id=id).order_by("id").all()
    return cards_schema.jsonify(cards)


@api.route("", methods=["POST"])
def new_game():
    data = request.get_json() or {}
    game_data = game_schema.load(data)
    game = Game(**game_data)
    db.session.add(game)
    db.session.commit()
    return game_schema.jsonify(game), 201


@api.route("/<string:id>", methods=["PATCH", "PUT"])
def update_game(id):
    game = Game.query.get(id)
    data = request.get_json()
    game_data = game_schema.load(data)
    for key, value in game_data.items():
        setattr(game, key, value)
    db.session.commit()
    return game_schema.jsonify(game)


@api.route("/<string:id>", methods=["DELETE"])
def delete_game(id):
    game = Game.query.get(id)
    db.session.delete(game)
    db.session.commit()
    return jsonify(""), 204
