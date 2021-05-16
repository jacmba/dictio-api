import unittest
from unittest.mock import patch
from data.db import DB


class test_db(unittest.TestCase):
    def setUp(self):
        self.db = DB("mongodb://mock")

    def test_object_creation(self):
        assert self.db.uri == "mongodb://mock"

    @patch("data.db.pymongo.MongoClient", return_value={"foo": "bar"})
    def test_client_connection(self, mock_MongoClient):
        self.db.connect()
        mock_MongoClient.assert_called_once_with("mongodb://mock")
        assert self.db.client["foo"] == "bar"
