import os
import logging
from typing import Any
from pathlib import Path

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from . import default_settings
from .utils import load_module_recursively


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(default_settings)
    if 'APP_CONFIG' in os.environ:
        app.config.from_envvar('APP_CONFIG', silent=False)
    else:
        config_local = Path(__file__).parent.parent.joinpath('config_local.py')
        app.config.from_pyfile(config_local, silent=True)

    if not app.debug:
        app.logger.setLevel(logging.INFO)

    return app


def configure_web():
    configure_login_manager()
    configure_views()


def configure_login_manager():
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        # pylint: disable=import-outside-toplevel
        from vault.services import UserService
        return UserService.get(id)


def configure_views():
    with app.app_context():
        # pylint: disable=import-outside-toplevel
        from vault import views
        load_module_recursively(views)


app = create_app()
db: Any = SQLAlchemy(app)
