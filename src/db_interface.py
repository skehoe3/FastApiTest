"""
This file contains all functions required to interact with the database.
"""

import pymongo
from bson.objectid import ObjectId


class Storage:

    def __init__(self):
        # ok so the DB is, in fact, there.  I can get to it over dbCompass
        self.client = pymongo.MongoClient('mongodb://localhost:27000/')
        self.db = self.client['fast-mongo']

    def insert_lyrics_v1(self, song):
        try:
            songs = self.db.songs
            self.db["songs"].insert_one(dict(song))
            return song
        except Exception as error:
            print(f"whoooa there: {error}")

    def get_song_v1(self, _id=None):
        try:
            if _id:
                return self.db["songs"].find_one(ObjectId(_id))
            return self.db["songs"].find()
        except Exception as error:
            print(f"whoooa there: {error}")
