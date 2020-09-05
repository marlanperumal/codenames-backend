from random import choice, shuffle

from sqlalchemy import func

from . import db, ma
from ..methods.utility import generate_id
from .cards import Card
from .words import Word
from .languages import Language

CARDS_PER_GAME = 25
GAME_ID_CHARACTERS = 6


class Game(db.Model):
    __tablename__ = "game"
    id = db.Column(db.String(20), primary_key=True)
    ready = db.Column(db.Boolean, default=False)
    active = db.Column(db.Boolean, default=True)
    complete = db.Column(db.Boolean, default=False)
    language_id = db.Column(db.String(5), db.ForeignKey("language.id"), index=True)

    cards = db.relationship("Card", backref="game", cascade="all, delete")
    language = db.relationship("Language", backref="languages")

    def __init__(self, **kwargs):
        super(Game, self).__init__(**kwargs)
        game_id = None
        while game_id is None or Game.query.get(game_id) is not None:
            game_id = generate_id(GAME_ID_CHARACTERS)

        self.id = game_id

        teams = (["BLUE"] * 8) + (["RED"] * 8) + (["NEUTRAL"] * 7) + ["DEATH"]
        teams += [choice(["BLUE", "RED"])]
        shuffle(teams)

        language_id = kwargs.get("language_id")
        self.language = Language.query.get(language_id)

        words = Word.query.filter_by(language_id=language_id).order_by(func.random()).limit(CARDS_PER_GAME)
        for word, team in zip(words, teams):
            card = Card(word=word.word, team=team, game=self)
            db.session.add(card)


class GameSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Game
        include_fk = True


game_schema = GameSchema()
games_schema = GameSchema(many=True)
