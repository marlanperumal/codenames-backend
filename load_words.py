import os
import argparse

from dotenv import load_dotenv

from codenames_backend import create_app
from codenames_backend.models import db
from codenames_backend.models.words import Word
from codenames_backend.models.languages import Language

parser = argparse.ArgumentParser(description="Load a Codenames Word List")
parser.add_argument("filename", type=str, help="Filename with words to load")
parser.add_argument(
    "--language",
    "-l",
    dest="language_id",
    type=str,
    default=None,
    help="Language code to be associated with the words e.g. EN, DE",
)
parser.add_argument(
    "--new-language",
    "-n",
    dest="new_language",
    action="store_true",
    default=False,
    help="Create language entry if it doesn't already exist",
)
parser.add_argument(
    "--truncate",
    "-t",
    dest="truncate",
    action="store_true",
    default=False,
    help="Truncate the existing word list if it doesn't already exist",
)

args = parser.parse_args()
language_id = args.language_id

if args.new_language and args.language_id is None:
    raise Exception("No language code provide to create")

load_dotenv()


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite:///app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


app = create_app(Config)

with app.app_context():
    if args.truncate:
        Word.query.delete()
    language = Language.query.get(language_id)
    if language is None:
        if args.new_language:
            language = Language(id=language_id)
            db.session.add(language)
        else:
            raise Exception(f"Language {language_id} does not exist. You might want the -n flag")
    else:
        if args.new_language:
            raise Exception(f"Cannot create new language {language_id} - already exists")
    with open(args.filename, "r") as f:
        for word in f:
            db.session.add(Word(word=word.strip(), language=language))
    db.session.commit()
