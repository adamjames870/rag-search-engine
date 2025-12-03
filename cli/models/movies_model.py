from typing import List
from typing import Any
from dataclasses import dataclass
import json
@dataclass
class Movie:
    id: int
    title: str
    description: str

    @staticmethod
    def from_dict(obj: Any) -> 'Movie':
        _id = int(obj.get("id"))
        _title = str(obj.get("title"))
        _description = str(obj.get("description"))
        return Movie(_id, _title, _description)

@dataclass
class MoviesData:
    movies: List[Movie]

    def __init__(self, movies=None):
        if movies is None:
            movies = []
        self.movies = movies

    @staticmethod
    def from_dict(obj: Any) -> 'Root':
        _movies = [Movie.from_dict(y) for y in obj.get("movies")]
        return MoviesData(_movies)

# Example Usage
# jsonstring = json.loads(myjsonstring)
# root = Root.from_dict(jsonstring)
