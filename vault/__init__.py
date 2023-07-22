import logging
import os
from pathlib import Path
from typing import TYPE_CHECKING, Any, Optional

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

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

    configure_logging(app)
    return app


def configure_logging(app: Flask):
    logging.basicConfig(format='[%(asctime)s] %(levelname)s %(name)s: %(message)s')
    logging.getLogger().setLevel(logging.INFO)

    if app.debug:
        logging.getLogger().setLevel(logging.DEBUG)

        # Make sure engine.echo is set to False
        logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

        # Fix werkzeug handler in debug mode
        logging.getLogger('werkzeug').handlers = []


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
