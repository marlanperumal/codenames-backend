from . import db, ma
from ..methods.utility import generate_id
from .games import Game

ROOM_ID_CHARACTERS = 6


class Room(db.Model):
    __tablename__ = "room"
    id = db.Column(db.String(20), primary_key=True)
    current_game_id = db.Column(db.String(20), db.ForeignKey("game.id"), index=True)

    current_game = db.relationship("Game", backref="rooms", uselist=False)

    def __init__(self):
        room_id = None
        while room_id is None or Room.query.get(room_id) is not None:
            room_id = generate_id(ROOM_ID_CHARACTERS)

        self.id = room_id

        game = Game()
        db.session.add(game)
        self.current_game = game


class RoomSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Room


room_schema = RoomSchema()
rooms_schema = RoomSchema(many=True)
