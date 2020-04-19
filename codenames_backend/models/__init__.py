from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)
ma = Marshmallow()
migrate = Migrate()

from .cards import Card  # noqa: F401
from .games import Game  # noqa: F401
from .words import Word  # noqa: F401
