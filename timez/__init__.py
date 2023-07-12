import json
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

key = os.urandom(24)
app = Flask(__name__)
# app.config.from_object('config.py')
app.config['SECRET_KEY'] = key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///timez.db'
db = SQLAlchemy(app)


# with app.app_context():
#     db.create_all()

from timez import routes

