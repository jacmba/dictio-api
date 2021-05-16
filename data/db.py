import pymongo


class DB:
    def __init__(self, uri, database) -> None:
        self.uri = uri
        self.database = database

    def connect(self):
        self.client = pymongo.MongoClient(self.uri)

    def find_alphabet(self):
        cols = self.client[self.database].list_collection_names()
        return cols