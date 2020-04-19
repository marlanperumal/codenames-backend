from . import db, ma


class Word(db.Model):
    __tablename__ = "word"
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(50))


class WordSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Word


word_schema = WordSchema()
words_schema = WordSchema(many=True)
