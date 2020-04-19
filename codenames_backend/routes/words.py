from flask import request, jsonify, Blueprint
from ..models import db
from ..models.words import Word, words_schema, word_schema

api = Blueprint("words", __name__)


@api.route("", methods=["GET"])
def get_words():
    words = Word.query.all()
    return words_schema.jsonify(words)


@api.route("", methods=["POST"])
def add_word():
    data = request.get_json()
    word_data = word_schema.load(data)
    word = Word(**word_data)
    db.session.add(word)
    db.session.commit()
    return word_schema.jsonify(word), 201


@api.route("/<int:id>", methods=["PATCH", "PUT"])
def update_word(id):
    word = Word.query.get(id)
    data = request.get_json()
    word_data = word_schema.load(data)
    for key, value in word_data.items():
        setattr(word, key, value)
    db.session.commit()
    return word_schema.jsonify(word)


@api.route("/<int:id>", methods=["DELETE"])
def delete_word(id):
    word = Word.query.get(id)
    db.session.delete(word)
    db.session.commit()
    return jsonify(""), 204
