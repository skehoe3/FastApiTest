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
from typing import Optional

class Song(BaseModel):
    artist: Optional[str] = None
    lyrics: str

app = FastAPI()
# logger = logging.basicConfig(level=__debug__)


@app.post("/lyrics/")
async def root(song_lyrics: Song):
    # logger.info("In post routine")
    print("woohooo we posted!")
    return song_lyrics #this returns empty though
