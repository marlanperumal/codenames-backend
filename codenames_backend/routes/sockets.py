from flask import request
from flask_socketio import SocketIO, send, emit, join_room, leave_room

from codenames_backend.models.cards import Card, cards_schema
from codenames_backend.models.players import Player, player_schema, players_schema
from codenames_backend.models.rooms import Room
from codenames_backend.models.games import Game, game_schema
from codenames_backend.models import db

socketio = SocketIO()


@socketio.on("connect")
def on_connect():
    player = Player(id=request.sid)
    db.session.add(player)
    db.session.commit()
    db.session.remove()


@socketio.on("disconnect")
def on_disconnect():
    player = Player.query.get(request.sid)
    room = player.current_room
    if room:
        message = f"{player.name} has left the room"
        print(message)
        send(message, room=room.id)
        players = Player.query.filter_by(
            current_room=room, active=True
        ).order_by("name").all()
        emit("players", players_schema.dump(players), room=room.id)

    player.current_room = None
    player.active = False
    db.session.commit()

    db.session.remove()


@socketio.on("join")
def on_join(data):
    player = Player.query.get(request.sid)
    room_id = data.get("room")
    room = Room.query.get(room_id)
    name = data.get("name")
    join_room(room_id)
    player.current_room = room
    player.name = name
    db.session.commit()

    game = room.current_game
    cards = Card.query.filter_by(game=game).order_by("id").all()
    emit("game", game_schema.dump(game))
    emit("cards", cards_schema.dump(cards))

    message = f"{player.name} has joined the room"
    print(message)
    send(message, room=room_id)

    players = Player.query.filter_by(
        current_room=room, active=True
    ).order_by("name").all()
    emit("players", players_schema.dump(players), room=room_id)
    db.session.remove()


@socketio.on("leave")
def on_leave(data):
    player = Player.query.get(request.sid)
    room = player.current_room
    leave_room(room.id)
    player.current_room = None
    player.current_team = "NEUTRAL"
    db.session.commit()

    message = f"{player.name} has left the room"
    print(message)
    send(message, room=room.id)

    players = Player.query.filter_by(
        current_room=room, active=True
    ).order_by("name").all()
    emit("players", players_schema.dump(players), room=room.id)

    db.session.remove()


@socketio.on("select-card")
def on_select_card(data):
    player = Player.query.get(request.sid)
    room = player.current_room
    game = room.current_game
    card_id = data.get("card")
    card = Card.query.get(card_id)
    if not card.selected:
        card.selected = True
        db.session.commit()
        cards = Card.query.filter_by(game=game).order_by("id").all()
        response = cards_schema.dump(cards)
        emit("cards", response, room=room.id)

        message = f"{player.name} picked {card.word.upper()}"
        print(message)
        send(message, room=room.id)

        db.session.remove()


@socketio.on("new-game")
def on_new_game():
    player = Player.query.get(request.sid)
    room = player.current_room
    game = Game(language_id=room.language_id)
    db.session.add(game)
    room.current_game = game
    for other_player in room.players:
        other_player.is_spymaster = False
    db.session.commit()
    cards = Card.query.filter_by(game=game).order_by("id").all()
    game_response = game_schema.dump(game)
    emit("game", game_response, room=room.id)
    cards_response = cards_schema.dump(cards)
    emit("cards", cards_response, room=room.id)

    message = f"{player.name} started a new game"
    print(message)
    send(message, room=room.id)

    players = Player.query.filter_by(
        current_room=room, active=True
    ).order_by("name").all()
    emit("players", players_schema.dump(players), room=room.id)

    db.session.remove()


@socketio.on("end-game")
def on_end_game():
    player = Player.query.get(request.sid)
    room = player.current_room
    game = room.current_game
    game.complete = True
    db.session.commit()
    game_response = game_schema.dump(game)
    emit("game", game_response, room=room.id)

    message = f"{player.name} ended the game"
    print(message)
    send(message, room=room.id)

    db.session.remove()


@socketio.on("switch-team")
def on_switch_team(data):
    player = Player.query.get(request.sid)
    room = player.current_room
    team = data.get("team")
    player.is_spymaster = False
    player.current_team = team
    db.session.commit()
    response = player_schema.dump(player)
    emit("player", response)

    message = f"{player.name} joined the {team.upper()} team"
    print(message)
    send(message, room=room.id)

    players = Player.query.filter_by(
        current_room=room, active=True
    ).order_by("name").all()
    emit("players", players_schema.dump(players), room=room.id)

    db.session.remove()


@socketio.on("toggle-spymaster")
def on_toggle_spymaster(data):
    player = Player.query.get(request.sid)
    room = player.current_room
    player.is_spymaster = data.get("is_spymaster")
    db.session.commit()
    response = player_schema.dump(player)
    emit("player", response)
    team = player.current_team

    if player.is_spymaster:
        message = f"{player.name} became a {team.upper()} spymaster"
    else:
        message = f"{player.name} became a normal {team.upper()} player"
    print(message)
    send(message, room=room.id)

    players = Player.query.filter_by(
        current_room=room, active=True
    ).order_by("name").all()
    emit("players", players_schema.dump(players), room=room.id)

    db.session.remove()
