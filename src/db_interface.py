"""
This file contains all functions required to interact with the database.
"""

import pymongo
from bson.objectid import ObjectId

# This assumes that mongodb is already running
# client = MongoClient()
# client = MongoClient('localhost', 27000)
# client = MongoClient('mongodb://localhost:27000/')

# TODO - actually connect this with pymongo
# TODO - there is no connection from Storage to pymongo


class Storage:

    def __init__(self):
        # ok so the DB is, in fact, there.  I can get to it over dbCompass
        self.client = pymongo.MongoClient('mongodb://localhost:27000/')
        self.db = self.client['fast-mongo']

# adjust to take in a dict
    def insert_lyrics_v1(self, song):
        try:
            songs = self.db.songs
            self.db["songs"].insert_one(dict(song))
            return dict(song)
        except Exception as error:
            print(f"whoooa there: {error}")

    def get_song_v1(self, _id=None):
        try:
            if _id:
                return self.db["songs"].find_one(ObjectId(_id))
            return self.db["songs"].find()
        except Exception as error:
            print(f"whoooa there: {error}")
