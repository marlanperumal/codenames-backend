from flask import request
from flask_socketio import SocketIO, send, emit, join_room, leave_room

from codenames_backend.models.cards import Card, cards_schema, card_schema
from codenames_backend.models.players import Player
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
        game = room.current_game
        if game:
            if game.blue_spymaster == player:
                message = "The blue spymaster has left the room" 
                game.ready = False
            elif game.red_spymaster == player:
                message = "The red spymaster has left the room"
                game.ready = False
            else:
                message = f"{player.name} has left the room"
            send(message, room=room.id)
    player.active = False
    db.session.commit()
    db.session.remove()


@socketio.on("join")
def on_join(data):
    room = data.get("room")
    name = data.get("name")
    team = data.get("team")
    player = Player.query.get(request.sid)

    join_room(room)
    print(f"{name} has joined the room")
    send(f"{name} has joined the room", room=room)
    # cards = Card.query.filter_by(game_id=room).order_by("id").all()
    # response = cards_schema.dump(cards)
    # emit("cards", response)
    db.session.remove()


@socketio.on("leave")
def on_leave(data):
    room = data["room"]
    leave_room(room)
    print("somebody has left the room")
    send("somebody has left the room", room=room)
    db.session.remove()


@socketio.on("select-card")
def on_select_card(data):
    room = data["room"]
    card_id = data["card"]
    card = Card.query.get(card_id)
    card.selected = not card.selected
    db.session.commit()
    response = card_schema.dump(card)
    emit("card", response, room=room)
    db.session.remove()
