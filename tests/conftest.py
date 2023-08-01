import os

import pytest
from dotenv import load_dotenv

from src.app import create_app

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
load_dotenv(dotenv_path=os.path.join(BASE_DIR, "../.env"))


@pytest.fixture(scope="session")
def client():
    app = create_app()
    app.config["TESTING"] = True
    app.testing = True
    with app.test_client() as client:
        with app.app_context():
            yield client
