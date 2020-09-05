"""
Author: Shannon Kehoe
Date: August 25, 2020

Basic intro of FastAPI found here: https://fastapi.tiangolo.com/tutorial/first-steps/

This file contains the endpoints of the service.  Any database interactions should be written in
db_interface.py, while any preprocessing actions should be written in preprocess.py.
"""
import logging


from fastapi import Body, FastAPI, File, UploadFile

from src.db_interface import Storage
from src.pydantic_models import Song
import json
import src.preprocess as preprocess

app = FastAPI()
DB = Storage()


@app.post("/v1/lyrics")
async def post_song(song_lyrics: Song):
    """
    Post endpoint to add a song to the DB
    Args:
        song_lyrics (Song): pdantic song object. see pydantic_models.py for details

    Returns:
        json: details on the song added to the db
    """
    try:
        song = DB.insert_lyrics_v1(song_lyrics)
        return {"_id": str(song_lyrics._id)}
    except Exception as error:
        return {"statusMessage": "Beep boop you made an oop", "Exception": error}


@app.get("/v1/lyrics")
async def get_songs():
    """
    Retrieves the details on all songs from the db

    Returns:
        json: all songs in db
    """
    try:
        return DB.get_many_songs_v1()
    except Exception as error:
        return {"statusMessage": "Beep boop you made an oop", "Exception": error}


@app.get("/v1/lyrics/{_id}")
async def get_song(_id: str):
    """
    Gets a specific song from the db

    Args:
        _id (str): ObjectId (in string form) for the song desired

    Returns:
        json: the specific song requested
    """
    try:
        return DB.get_song_v1(_id)
    except Exception as error:
        return {"statusMessage": "Beep boop you made an oop", "Exception": error}


@app.post("/v1/fileToDb")
async def csv_to_db(file: UploadFile = File(...), db_name: str = Body(...)):
    # this endpoint takes in a file of type csv, parses it, and adds
    # each entry to the db
    #! currently everything is held in memory for some stupid reason....
    #! use the rollover function to put a stop to that nonesense
    print("took in the file!")
    # file is here still an UploadFile object... convert to bytes object before sending to preproces
    formatted = preprocess.csv_to_json(file.file, db_name)

    pass
