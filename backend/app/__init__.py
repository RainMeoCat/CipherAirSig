import logging
from logging.handlers import TimedRotatingFileHandler

from flask import Flask
from flask_cors import CORS

from app.commands import create_tables, del_user, delete_tables
from app.extinsions import db, migrate
from app.server import server


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_pyfile('config.py')
    app.debug = True

    formatter = logging.Formatter(
        "[%(asctime)s][%(filename)s:%(lineno)d][%(levelname)s][%(thread)d] - %(message)s")
    handler = TimedRotatingFileHandler(
        "flask.log", when="D", interval=1, backupCount=10,
        encoding="UTF-8", delay=False, utc=True)
    handler.setLevel(logging.DEBUG)
    app.logger.addHandler(handler)
    handler.setFormatter(formatter)


    from app.user import models
    from app.token import models
    from app.gesturesign import models

    db.init_app(app)
    migrate.init_app(app, db)
    from app.user import user

    from app.token import token
    from app.gesturesign import gsign

    app.register_blueprint(user, url_prefix='/api/user')
    app.register_blueprint(server, url_prefix='/api/server')
    app.register_blueprint(token, url_prefix='/api/token')
    app.register_blueprint(gsign, url_prefix='/api/gsign')

    app.cli.add_command(create_tables)
    app.cli.add_command(delete_tables)
    app.cli.add_command(del_user)

    return app
