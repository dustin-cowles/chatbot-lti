import json
import logging
import os

from asgiref.wsgi import WsgiToAsgi
from flask import Flask

from lib.cache import get_app_cache
from lib.lti import get_launch_data_storage, export_jwks


def setup_app(app_name, template_folder="templates", static_folder="static"):
    """
    Creates a Flask app and configures the Flask app,
    asgi app, logging, and exports the jwks file.

    :param app: The Flask application instance name.

    :return: app
    :rtype: Flask application instance.
    :return: asgi_app
    :rtype: Asgi application instance.
    :return: get_launch_data_storage()
    :rtype: LTI Launch Session Storage
    :return: cache
    :rtype: Flask Cache service instance.
    """
    configure_logging()
    export_jwks()

    app = Flask(
        app_name,
        template_folder=template_folder,
        static_folder=static_folder)
    app.config.from_file(os.path.join(
        "config", "flask_config.json"), load=json.load)
    logging.debug("Flask Config: %s", app.config)

    asgi_app = WsgiToAsgi(app)
    cache = get_app_cache(app)

    return app, asgi_app, get_launch_data_storage(cache), cache


def configure_logging():
    """
    Configures the Python logging module.

    :params: None

    :return: None
    """
    logging.getLogger().setLevel(10)
