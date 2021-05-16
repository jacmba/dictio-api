import pymongo


class DB:
    def __init__(self, uri) -> None:
        self.uri = uri

    def connect(self):
        self.client = pymongo.MongoClient(self.uri)
