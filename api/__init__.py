from flask import Flask
from flask_smorest import Api, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
db_name = 'smafs.db'

app = Flask(__name__)
app.app_context().push()

# SQLAlchemy configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, db_name)
app.config['SECRET_KEY'] = os.urandom(24)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Api configuration
app.config["API_TITLE"] = "My API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.2"
api = Api(app)

from .auth.views import auth
api.register_blueprint(auth)