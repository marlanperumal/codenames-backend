from random import choices, choice, shuffle
from string import ascii_uppercase, digits

from sqlalchemy import func

from . import db, ma
from .cards import Card
from .words import Word

CARDS_PER_GAME = 25
GAME_ID_CHARACTERS = 6


def generate_id():
    return ''.join(choices(ascii_uppercase + digits, k=GAME_ID_CHARACTERS))


class Game(db.Model):
    __tablename__ = "game"
    id = db.Column(db.String(20), primary_key=True)

    cards = db.relationship("Card", backref="game", cascade="all, delete")

    def __init__(self):
        game_id = None
        while game_id is None or Game.query.get(game_id) is not None:
            game_id = generate_id()

        self.id = game_id

        teams = (["blue"] * 8) + (["red"] * 8) + (["neutral"] * 7) + ["death"]
        teams += [choice(["blue", "red"])]
        shuffle(teams)

        words = Word.query.order_by(func.random()).limit(CARDS_PER_GAME)
        for word, team in zip(words, teams):
            card = Card(
                word=word.word,
                team=team,
                game=self
            )
            db.session.add(card)


class GameSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Game


game_schema = GameSchema()
games_schema = GameSchema(many=True)
