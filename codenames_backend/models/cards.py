from . import db, ma


class Card(db.Model):
    __tablename__ = "card"
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(50))
    selected = db.Column(db.Boolean, default=False)
    team = db.Column(db.String(50))
    game_id = db.Column(db.String(50), db.ForeignKey("game.id"), index=True)


class CardSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Card


card_schema = CardSchema()
cards_schema = CardSchema(many=True)
