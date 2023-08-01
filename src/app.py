from flask import Flask
from flask_restx import Api as ApiRestx

from src.api.routes import register_endpoints_routes
from src.default_config import DefaultConfig


def create_app():
    app = Flask(__name__)

    DefaultConfig.init_loggers()
    app.config.from_object(DefaultConfig)

    apix = ApiRestx(
        app,
        prefix=DefaultConfig.PREFIX_PATH,
        title="Tor IP addresses backend",
    )

    register_endpoints_routes(apix)

    return app

