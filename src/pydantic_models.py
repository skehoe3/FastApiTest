from typing import List, Optional

from bson.objectid import ObjectId
from pydantic import BaseModel, validator


class Song(BaseModel):
    artist: str = None
    lyrics: str
    category: List[str]
    title: Optional[str]
    _id = ObjectId()

    # todo: set up a logger

    @validator("lyrics", "artist", "category", "title")
    def non_empty(cls, v):
        #! CANNOT do on category as category is a list!
        if len(v) == 0:
            print("hello ", str(set(v)))
            raise ValueError(
                "Value cannot be empty!")
        return v

    @validator("lyrics", "artist", "title")
    def more_than_whitespace(cls, v):
        if v.isspace():
            raise ValueError(
                "Value cannot be only strings!")

    @validator("category")
    def list_has_strings(cls, v):
        # todo ensure each value of list is a string
        are_strings = [isinstance(x, str) for x in v]
        #! FastAPI converts everything to a string!
        # ? Should we allow this?
        if False in are_strings:
            raise ValueError(
                "List must only contain strings!")
