from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from timez.config import Config


db = SQLAlchemy()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from timez.main.routes import main
    from timez.contacts.routes import contacts
    from timez.time.routes import time
    from timez.errors.handlers import errors
    app.register_blueprint(main)
    app.register_blueprint(contacts)
    app.register_blueprint(time)
    app.register_blueprint(errors)

    return app
