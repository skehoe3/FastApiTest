"""
This file contains all functions required to interact with the database.
"""

import pymongo
from bson.objectid import ObjectId
from collections import defaultdict


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
            resp = defaultdict()
            result = self.db["songs"].find_one(ObjectId(_id))
            # todo refactor as dictionary comprehension
            for i in result.keys():
                resp[i] = str(result[i]) if isinstance(
                    result[i], ObjectId) else result[i]
            return resp
        except Exception as error:
            print(f"whoooa there: {error}")

    def get_many_songs_v1(self):
        try:
            resp = []

            result = self.db["songs"].find({})
            for i in result:
                resp.append({x: (str(i[x]) if isinstance(i[x], ObjectId) else i[x])
                             for x in i.keys()})
            return {"result": resp}

        except Exception as error:
            print(f"whoooa there: {error}")
