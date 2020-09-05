from . import db, ma


class Language(db.Model):
    __table_name__ = "language"

    id = db.Column(db.String(5), primary_key=True)
    language_name = db.Column(db.String(255))


class LanguageSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Language


language_schema = LanguageSchema()
languages_schema = LanguageSchema(many=True)
