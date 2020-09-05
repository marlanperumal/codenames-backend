from flask import request, jsonify, Blueprint
from ..models import db
from ..models.languages import Language, languages_schema, language_schema

api = Blueprint("languages", __name__)


@api.route("", methods=["GET"])
def get_languages():
    languages = Language.query.all()
    return languages_schema.jsonify(languages)


@api.route("", methods=["POST"])
def add_language():
    data = request.get_json()
    language_data = language_schema.load(data)
    language = Language(**language_data)
    db.session.add(language)
    db.session.commit()
    return language_schema.jsonify(language), 201


@api.route("/<int:id>", methods=["PATCH", "PUT"])
def update_language(id):
    language = Language.query.get(id)
    data = request.get_json()
    language_data = language_schema.load(data)
    for key, value in language_data.items():
        setattr(language, key, value)
    db.session.commit()
    return language_schema.jsonify(language)


@api.route("/<int:id>", methods=["DELETE"])
def delete_language(id):
    language = Language.query.get(id)
    db.session.delete(language)
    db.session.commit()
    return jsonify(""), 204
