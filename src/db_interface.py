"""
This file contains all functions required to interact with the database.
"""

import pymongo
from bson.objectid import ObjectId
from collections import defaultdict


class Storage:

    def __init__(self):
        self.client = pymongo.MongoClient('mongodb://localhost:27000/')
        self.db = self.client['fast-mongo']

    def insert_value(self, val, database):
        """
        insert a single value into the db

        Args:
            val (json): data to be inserted
            database (str): name of the db the data should be added to
        """
        self.db[database].insert_one(dict(val))

    def insert_multiple_values(self, vals, database):
        """
        insert a single value into the db

        Args:
            val (list): list of json data points to be inserted
            database (str): name of the db the data should be added to
        """
        self.db[database].insert_many(vals)

    def insert_lyrics_v1(self, song):
        """
        Add lyrics to db
        Args:
            song (obj): pydantic song object

        Returns:
            dict: data from the db
        """
        try:
            songs = self.db.songs
            self.db["songs"].insert_one(dict(song))
            return song
        except Exception as error:
            print(f"whoooa there: {error}")

    def get_song_v1(self, _id):
        """
        Get a single song from the db

        Args:
            _id (string, optional): ObjectId in string form for a song in the db

        Returns:
            dict: details of the song
        """
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
        """
        get the details for all songs in the db
        Returns:
            dict: dictionary of all songs in the db
        """
        try:
            resp = []

            result = self.db["songs"].find({})
            for i in result:
                resp.append({x: (str(i[x]) if isinstance(i[x], ObjectId) else i[x])
                             for x in i.keys()})
            return {"result": resp}

        except Exception as error:
            print(f"whoooa there: {error}")
