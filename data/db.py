import pymongo
from pymongo import database


class DB:
    def __init__(self, uri, database) -> None:
        self.uri = uri
        self.database = database

    def connect(self):
        self.client = pymongo.MongoClient(self.uri)

    def find_alphabet(self):
        cols = self.client[self.database].list_collection_names()
        cols = list(filter(lambda x: len(x) == 1, cols))
        cols = list(map(lambda x: x.upper(), cols))
        cols = sorted(cols)
        return cols

    def find_word(self, letter, word):
        definition = self.client[self.database][letter].find_one(
            {"word": word})
        return definition
