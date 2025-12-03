
from .clean_keywords import clean_keywords, clean_titles
from .search_utils import load_movies, keyword_in_words
from models.movies_model import MoviesData

def keyword_search(search_string: str, max_results: int) -> MoviesData:

    movies_data = load_movies()
    found_movies = MoviesData()
    keywords = clean_keywords(search_string)

    for this_movie in movies_data.movies:
        title_words = clean_titles(this_movie.title)
        if keyword_in_words(keywords, title_words):
            found_movies.movies.append(this_movie)
        if len(found_movies.movies) >= max_results:
            break

    found_movies.movies = sorted(found_movies.movies, key=lambda movie: movie.id, reverse=True)
    return found_movies