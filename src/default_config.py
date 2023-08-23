import os
from logging.config import dictConfig

from dotenv import load_dotenv


class DefaultConfig:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    load_dotenv(dotenv_path=os.path.join(BASE_DIR, "../.env"))

    DEBUG = os.environ.get("DEBUG")
    BUNDLE_ERRORS = True
    MODE = os.environ.get("MODE")

    # api prefix
    PREFIX_PATH = "/{}".format(os.environ.get("DEPLOYMENT_VERSION"))

    # USER_AGENT
    USER_AGENT = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,"
        " like Gecko) Chrome/111.0.0.0 Safari/537.36"
    )
    # torip  database
    DATABASE = {
        "name": os.environ.get("POSTGRESQL_DB_NAME"),
        "engine": os.environ.get("POSTGRESQL_DB_ENGINE"),
        "user": os.environ.get("POSTGRESQL_DB_USER"),
        "password": os.environ.get("POSTGRESQL_DB_PASSWD"),
        "host": os.environ.get("POSTGRESQL_DB_HOST"),
        "port": os.environ.get("POSTGRESQL_DB_PORT"),
    }
    DATABASE_URL = os.environ.get("DATABASE_URL")

    UDGER_URL = "https://udger.com/resources/ip-list/tor_exit_node"
    DAN_URL = "https://www.dan.me.uk/tornodes"

    PROPAGATE_EXCEPTIONS = True

    @staticmethod
    def init_loggers():
        LOGGING = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "verbose": {
                    "format": (
                        "%(levelname)s -- %(asctime)s --"
                        " %(pathname)s:%(lineno)d >  %(message)s "
                    ),
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                },
            },
            "handlers": {
                "console": {
                    "level": "DEBUG",
                    "class": "logging.StreamHandler",
                    "stream": "ext://flask.logging.wsgi_errors_stream",
                    "formatter": "verbose",
                },
                "file": {
                    "level": "INFO",
                    "class": "logging.handlers.RotatingFileHandler",
                    "filename": "/tmp/torip-api.log",
                    "mode": "a",
                    "maxBytes": 10485760,
                    "backupCount": 10,
                    "formatter": "verbose",
                },
            },
            "loggers": {
                "flask_restx": {
                    "level": "DEBUG",
                    "handlers": ["console", "file"],
                },
                "torip_test_backend": {
                    "level": "DEBUG",
                    "handlers": ["console", "file"],
                },
            },
        }
        dictConfig(LOGGING)
