from flask_socketio import SocketIO, send, emit, join_room, leave_room

from codenames_backend.models.cards import Card, cards_schema, card_schema
from codenames_backend.models import db

socketio = SocketIO()


@socketio.on("join")
def on_join(data):
    room = data["room"]
    join_room(room)
    print("somebody has joined the room")
    send("somebody has joined the room", room=room)
    cards = Card.query.filter_by(game_id=room).order_by("id").all()
    response = cards_schema.dump(cards)
    emit("cards", response)


@socketio.on("leave")
def on_leave(data):
    room = data["room"]
    leave_room(room)
    print("somebody has left the room")
    send("somebody has left the room", room=room)


@socketio.on("select-card")
def on_select_card(data):
    room = data["room"]
    card_id = data["card"]
    card = Card.query.get(card_id)
    card.selected = not card.selected
    db.session.commit()
    response = card_schema.dump(card)
    emit("card", response, room=room)
