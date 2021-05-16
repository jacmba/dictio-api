import unittest
from unittest.mock import patch
from data.db import DB


class test_db(unittest.TestCase):
    def setUp(self):
        self.db = DB("mongodb://mock", "mock")

    def test_object_creation(self):
        assert self.db.uri == "mongodb://mock"
        assert self.db.database == "mock"

    @patch("data.db.pymongo.MongoClient", return_value={"foo": "bar"})
    def test_client_connection(self, mock):
        self.db.connect()
        mock.assert_called_once_with("mongodb://mock")
        assert self.db.client["foo"] == "bar"

    @patch("data.db.pymongo.MongoClient",
           return_value={
               "mock": {
                   "list_collection_names": lambda: ["A", "B", "C"]
               }
           })
    def test_find_alphabet(self, mock):
        self.db.connect()
        result = self.db.find_alphabet()
        assert result == ["A", "B", "C"]
