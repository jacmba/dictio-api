import unittest
from unittest.mock import patch
from data.db import DB


class mockDb:
    def list_collection_names(self):
        return ["A", "B", "wrong", "C"]


class mockColl:
    def find_one(self, query, project):
        return {"definition": "lorem ipsum dolor sit amet"}

    def aggregate(self, pipeline):
        return [{"definition": "random word"}]


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

    @patch("data.db.pymongo.MongoClient", return_value={"mock": mockDb()})
    def test_find_alphabet(self, mock):
        self.db.connect()
        result = self.db.find_alphabet()
        assert result == ["A", "B", "C"]

    @patch("data.db.pymongo.MongoClient",
           return_value={"mock": {
               "a": mockColl()
           }})
    def test_find_word(self, mock):
        self.db.connect()
        result = self.db.find_word("a", "whatever")
        assert result["definition"] == "lorem ipsum dolor sit amet"

    @patch("data.db.pymongo.MongoClient",
           return_value={"mock": {
               "a": mockColl()
           }})
    def test_find_random_word(self, mock):
        self.db.connect()
        result = self.db.find_random_word("a")
        assert result[0]["definition"] == "random word"

    @patch("data.db.DB.find_alphabet", return_value=["A", "B", "C"])
    @patch("data.db.DB.find_random_word",
           return_value=[{
               "definition": "mock random word"
           }])
    def test_find_random_dictionary(self, mock_alphabet, mock_word):
        self.db.connect()
        result = self.db.find_random_dictionary()
        assert len(result) == 3
        assert result["a"]["definition"] == "mock random word"
