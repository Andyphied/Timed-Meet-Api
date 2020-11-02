from flask import Flask
from core.config import Config, setting
from flask_migrate import Migrate, MigrateCommand
from flask_jwt_extended import JWTManager
from flask_smorest import Api
from flask_cors import CORS

migrate = Migrate()
jwt = JWTManager()
cors = CORS()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config["API_TITLE"] = setting.API_TITLE
    app.config["API_VERSION"] = setting.API_VERSION
    app.config["JWT_SECRET_KEY"] = setting.JWT_SECRET_KEY
    api = Api(app)

    from models import db

    db.init_app(app)
    app.db = db

    migrate.init_app(app, db)
    app.cli.add_command(MigrateCommand, name="db")

    jwt.init_app(app)

    from schema import ma

    ma.init_app(app)

    cors.init_app(app)

    from api import user_blp, auth_blp, agenda_blp, meeting_blp

    api.register_blueprint(user_blp)
    api.register_blueprint(auth_blp)
    api.register_blueprint(agenda_blp)
    api.register_blueprint(meeting_blp)

    return app
