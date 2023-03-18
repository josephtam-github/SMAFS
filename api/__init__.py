from dotenv import load_dotenv
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_smorest import Api, Blueprint
from flask_sqlalchemy import SQLAlchemy
from .config.config import config_dict
from .utils import db, ma
from .models.blocklist import TokenBlocklist
from .models.user import User
from .models.course import Course
from .models.record import Record


def create_app(config=config_dict['dev']):
    app = Flask(__name__)

    app.config.from_object(config)


    db.init_app(app)
    ma.init_app(app)
    migrate = Migrate(app, db)

    app.config["API_TITLE"] = "My API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.2"
    api = Api(app)

    jwt = JWTManager(app)

    # Callback function to check if a JWT exists in the database blocklist
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
        jti = jwt_payload["jti"]
        token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()

        return token is not None

    # Import blueprints at end of file to prevent circular import
    from .auth.views import auth
    from .students.views import student
    from .courses.views import course
    from .record.views import record
    api.register_blueprint(auth)
    api.register_blueprint(student)
    api.register_blueprint(course)
    api.register_blueprint(record)

    @app.shell_context_processor
    def make_shell_context():
        return {
            'db': db,
            'ma': ma,
            'User': User,
            'Course': Course,
            'Record': Record,
        }

    return app
