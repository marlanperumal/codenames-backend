__version__ = "0.1.0"

from flask import Flask

from .models import db, ma, migrate
from .routes.cards import api as cards_api
from .routes.words import api as words_api
from .routes.games import api as games_api
from .routes.rooms import api as rooms_api
from .routes.errors import api as error_api
from .routes.sockets import socketio


def create_app(config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config)
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    socketio.init_app(app, cors_allowed_origins="*", logger=True)
    app.register_blueprint(cards_api, url_prefix="/api/cards")
    app.register_blueprint(words_api, url_prefix="/api/words")
    app.register_blueprint(games_api, url_prefix="/api/games")
    app.register_blueprint(rooms_api, url_prefix="/api/rooms")
    app.register_blueprint(error_api)
    return app
