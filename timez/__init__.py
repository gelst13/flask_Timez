import os
from flask import Flask
from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy
from timez.config import Config


key = os.urandom(24)
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)


# with app.app_context():
#     db.create_all()

from timez import routes
from timez.errors.handlers import errors
app.register_blueprint(errors)

