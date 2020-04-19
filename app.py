import os

from codenames_backend import create_app




# from flask_socketio import SocketIO, send



class Config():
    SECRET_KEY = os.getenv("SECRET_KEY", "secret123!")
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite:///instance/app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

app = create_app(Config)

# socketio = SocketIO(app)





# @socketio.on("connect")
# def test_connect():
#     send("connection received")


# if __name__ == "__main__":
#     socketio.run(app)
