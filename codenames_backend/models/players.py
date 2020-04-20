from . import db, ma


class Player(db.Model):
    __tablename__ = "player"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    team = db.Column(db.String(50))
    game_id = db.Column(db.String(50), db.ForeignKey("game.id"), index=True)


class PlayerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Player


player_schema = PlayerSchema()
players_schema = PlayerSchema(many=True)
