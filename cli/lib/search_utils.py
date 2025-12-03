import json

from models.movies_model import MoviesData

MOVIES_FILEPATH = "./data/movies.json"

def load_movies() -> MoviesData:

    with open(MOVIES_FILEPATH, 'r') as file:
        data = json.load(file)

    return MoviesData.from_dict(data)