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
            {"word": word}, {
                "_id": 0,
                "word": 1,
                "definition": 1
            })
        return definition

    def find_random_word(self, letter):
        pipeline = [{
            "$sample": {
                "size": 1
            }
        }, {
            "$project": {
                "_id": 0,
                "letters": 0
            }
        }]
        definition = self.client[self.database][letter].aggregate(pipeline)
        return list(definition)

    def find_random_dictionary(self):
        result = dict()
        letters = self.find_alphabet()
        for l in letters:
            word = self.find_random_word(l.lower())
            result[l.lower()] = word[0]
        return result
