"""
Author: Shannon Kehoe
Date: August 25, 2020

Basic intro of FastAPI found here: https://fastapi.tiangolo.com/tutorial/first-steps/

This file contains the endpoints of the service.  Any database interactions should be written in
db_interface.py, while any preprocessing actions should be written in preprocess.py.
"""
from fastapi import FastAPI, Body
import logging
from pydantic import BaseModel
from typing import Optional, List
import db_interface
from bson.objectid import ObjectId

class Song(BaseModel):
    artist: Optional[str] = None
    lyrics: str
    category: List[str]
    _id = ObjectId()


app = FastAPI()
DB = db_interface.Storage()
# logger = logging.basicConfig(level=__debug__)


@app.post("/lyrics/")
async def root(song_lyrics: Song):

    #return song_lyrics #this returns empty though
    try:
        song = DB.insert_lyrics(song_lyrics)
        return song
    #!part of the problem is i send over a ditionary i think
    except Exception as error:
        return {"Error": "Beep boop you made an oop", "Exception": error}