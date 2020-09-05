from . import db, ma
from ..methods.utility import generate_id
from .games import Game
from .languages import Language

ROOM_ID_CHARACTERS = 6


class Room(db.Model):
    __tablename__ = "room"
    id = db.Column(db.String(20), primary_key=True)
    current_game_id = db.Column(db.String(20), db.ForeignKey("game.id"), index=True)
    language_id = db.Column(db.String(5), db.ForeignKey("language.id"), index=True)

    current_game = db.relationship("Game", backref="rooms", uselist=False)
    language = db.relationship("Language", backref="rooms")

    def __init__(self, **kwargs):
        super(Room, self).__init__(**kwargs)
        room_id = None
        while room_id is None or Room.query.get(room_id) is not None:
            room_id = generate_id(ROOM_ID_CHARACTERS)

        self.id = room_id
        language_id = kwargs.get("language_id")
        self.language = Language.query.get(language_id)

        game = Game(language_id=language_id)
        db.session.add(game)
        self.current_game = game


class RoomSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Room
        include_fk = True

    id = ma.auto_field(dump_only=True)


room_schema = RoomSchema()
rooms_schema = RoomSchema(many=True)
