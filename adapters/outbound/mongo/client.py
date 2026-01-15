from pymongo import MongoClient


class MongoClientProvider:
    def __init__(self, uri: str, db_name: str):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]


    def get_db(self):
        return self.db