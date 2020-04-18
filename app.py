import os

from flask import Flask, request, jsonify, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
# from flask_socketio import SocketIO, send

app = Flask(__name__)
SECRET_KEY = os.getenv("SECRET_KEY", "secret123!")
SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite:///app.db")
app.config["SECRET_KEY"] = SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# socketio = SocketIO(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)
Migrate(app, db)


class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(50))
    selected = db.Column(db.Boolean, default=False)
    team = db.Column(db.String(50))
    game_id = db.Column(db.String(50), index=True)


class CardSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Card


card_schema = CardSchema()
cards_schema = CardSchema(many=True)

api = Blueprint("api", __name__)


@api.route("/cards", methods=["GET"])
def get_cards():
    game_id = request.args.get("game_id")
    query = Card.query
    if game_id:
        query = query.filter_by(game_id=game_id)
    query = query.order_by("id")
    cards = query.all()
    return cards_schema.jsonify(cards)


@api.route("/cards", methods=["POST"])
def add_card():
    data = request.get_json()
    card_data = card_schema.load(data)
    card = Card(**card_data)
    db.session.add(card)
    db.session.commit()
    return card_schema.jsonify(card), 201


@api.route("/cards/<int:id>", methods=["PATCH", "PUT"])
def update_card(id):
    card = Card.query.get(id)
    data = request.get_json()
    card_data = card_schema.load(data)
    for key, value in card_data.items():
        setattr(card, key, value)
    db.session.commit()
    return card_schema.jsonify(card)


@api.route("/cards/<int:id>", methods=["DELETE"])
def delete_card(id):
    card = Card.query.get(id)
    db.session.delete(card)
    db.session.commit()
    return jsonify(""), 204


app.register_blueprint(api, url_prefix="/api")


# @socketio.on("connect")
# def test_connect():
#     send("connection received")


# if __name__ == "__main__":
#     socketio.run(app)
