from . import db, ma


class Player(db.Model):
    __table_name__ = "player"
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(20))
    active = db.Column(db.Boolean, index=True, default=True)
    current_room_id = db.Column(db.String(20), db.ForeignKey("room.id"), index=True)
    current_team = db.Column(db.String(20), index=True)

    current_room = db.relationship("Room", backref="players")


class PlayerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Player


player_schema = PlayerSchema()
players_schema = PlayerSchema(many=True)