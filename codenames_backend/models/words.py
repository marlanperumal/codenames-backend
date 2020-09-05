from . import db, ma


class Word(db.Model):
    __tablename__ = "word"
    __table_args__ = (
        db.UniqueConstraint("word", "language_id"),
    )
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(50))
    language_id = db.Column(db.String(5), db.ForeignKey("language.id"), index=True)

    language = db.relationship("Language", backref="words")


class WordSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Word
        include_fk = True


word_schema = WordSchema()
words_schema = WordSchema(many=True)
