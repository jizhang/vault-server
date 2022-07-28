import os
import logging
from typing import TYPE_CHECKING, Any, Optional
from pathlib import Path

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from . import default_settings

if TYPE_CHECKING:
    from vault.models.user import User


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(default_settings)
    if 'APP_CONFIG' in os.environ:
        app.config.from_envvar('APP_CONFIG', silent=False)
    else:
        config_local = Path(__file__).parent.parent.joinpath('config_local.py')
        app.config.from_pyfile(str(config_local), silent=True)

    if not app.debug:
        app.logger.setLevel(logging.INFO)

    return app


def configure_web() -> None:
    configure_login_manager()
    configure_views()


def configure_login_manager() -> None:
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id: str) -> Optional['User']:
        # pylint: disable=import-outside-toplevel
        from vault.services import user as user_svc
        return user_svc.get_user(user_id)


def configure_views() -> None:
    with app.app_context():
        # pylint: disable=import-outside-toplevel
        from vault import views
        from vault.utils import load_module_recursively
        load_module_recursively(views)


app = create_app()
db: Any = SQLAlchemy(app)
