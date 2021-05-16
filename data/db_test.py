from data.db import DB
import pytest
from unittest.mock import patch


@pytest.fixture
def db():
    return DB("mongo://mock")


def test_db_object(db):
    assert db.uri == "mongo://mock"


@patch("pymongo.MongoClient")
def test_client_connection(db):
    db.connect()
    assert db.client["foo"] == "bar"
