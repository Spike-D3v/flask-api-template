import pytest

from app import create_app
from app.db import db


@pytest.fixture()
def app():
    app_ = create_app("config.testing")
    ctx = app_.test_request_context()
    ctx.push()

    with app_.app_context():
        db.create_all()

    yield app_

    with app_.app_context():
        db.drop_all()
    ctx.pop()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
