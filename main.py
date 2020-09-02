"""
Author: Shannon Kehoe
Date: August 25, 2020

Basic intro of FastAPI found here: https://fastapi.tiangolo.com/tutorial/first-steps/

This file contains the endpoints of the service.  Any database interactions should be written in
db_interface.py, while any preprocessing actions should be written in preprocess.py.
"""
import logging


from fastapi import Body, FastAPI

from src.db_interface import Storage
from src.pydantic_models import Song


app = FastAPI()
DB = Storage()
# logger = logging.basicConfig(level=__debug__)

#! this is returing null when it should be raising an exception as its missing mandatory values


@app.post("/v1/lyrics/")
async def post_song(song_lyrics: Song):

    # return song_lyrics #this returns empty though
    try:
        song = DB.insert_lyrics_v1(song_lyrics)
        return {"_id": str(song_lyrics._id)}
    #!part of the problem is i send over a dictionary i think
    except Exception as error:
        return {"statusMessage": "Beep boop you made an oop", "Exception": error}


@app.get("/v1/lyrics/{_id}")
async def get_song(_id: str):
    try:
        return DB.get_song_v1(_id)

    except Exception as error:
        return {"statusMessage": "Beep boop you made an oop", "Exception": error}
