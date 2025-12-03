from .search_utils import load_movies
from models.movies_model import MoviesData

def keyword_search(keyword: str, max_results: int) -> MoviesData:

    movies_data = load_movies()
    found_movies = MoviesData()

    for this_movie in movies_data.movies:
        if keyword in this_movie.title:
            found_movies.movies.append(this_movie)
        if len(found_movies.movies) >= max_results:
            break

    found_movies.movies = sorted(found_movies.movies, key=lambda movie: movie.id, reverse=True)
    return found_movies