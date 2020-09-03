from typing import List, Optional

from bson.objectid import ObjectId
from pydantic import BaseModel, validator

# some values are optional, and if not explicitly passed *are* allowed
# to be null.  As such, we don't use the * notation to check for validity


class Song(BaseModel):
    artist: Optional[str]
    lyrics: str
    category: List[str]
    title: Optional[str]
    _id = ObjectId()
    # timestamp

    # todo: set up a logger

    @validator("lyrics", "artist", "category", "title")
    def non_empty(cls, v):
        #! CANNOT do on category as category is a list!
        if len(v) == 0:
            raise ValueError(
                "Value cannot be empty!")
        return v

    @validator("category")
    def list_has_strings(cls, v):
        # todo ensure each value of list is a string
        are_strings = [isinstance(x, str) for x in v]
        #! FastAPI converts everything to a string!
        # ? Should we allow this?
        if False in are_strings:
            raise ValueError(
                "List must only contain strings!")
