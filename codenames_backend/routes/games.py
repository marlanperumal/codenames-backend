from flask import request, jsonify, Blueprint, current_app
from ..models import db
from ..models.cards import Card, cards_schema
from ..models.games import Game, games_schema, game_schema
from ..models.players import Player

from sqlalchemy.orm.exc import *

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
    game = Game()
    db.session.add(game)
    db.session.commit()
    return game_schema.jsonify(game), 201


@api.route("/join", methods=["POST"])
def new_game_with_user():
    json = request.json
    
    if "player" not in json:
        return "No player provided", 500
    else:
        player_name = json["player"]

    if "gameId" not in json or json["gameId"] is None:
        current_app.logger.info("Creating a new game")
        game = Game()
        player = Player()
        player.name = player_name
        player.game_id = game.id
        player.team = "blue"
        player.captain = True
        db.session.add(game)
        db.session.add(player)
        db.session.commit()

    else:
        game_id = json["gameId"]
        current_app.logger.info("Joining existing game {}".format(game_id))

        try:
            game = db.session.query(Game).filter(Game.id == game_id).one()
        except NoResultFound as e:
            current_app.logger.info("Could not find game {} {}".format(gameId, e))
            return { "error": "Game could not be found" }, 500

        try:
            player = (
                db.session.query(Player)
                .filter(Player.name == player_name)
                .filter(Player.game_id == game_id)
                .one()
            )
        except NoResultFound:
            current_app.logger.info("Adding player {} to game {}".format(player_name, game.id))
            player = Player()
            player.name = player_name
            player.game_id = game.id
            player.team = "blue"
            db.session.add(player)
            db.session.commit()
    
    return { 
        "gameId": game.id,
        "player": player.name
    }, 200


@api.route("/<int:id>", methods=["PATCH", "PUT"])
def update_game(id):
    game = Game.query.get(id)
    data = request.get_json()
    game_data = game_schema.load(data)
    for key, value in game_data.items():
        setattr(game, key, value)
    db.session.commit()
    return game_schema.jsonify(game)


@api.route("/<int:id>", methods=["DELETE"])
def delete_game(id):
    game = Game.query.get(id)
    db.session.delete(game)
    db.session.commit()
    return jsonify(""), 204
