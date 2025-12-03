
from .clean_keywords import clean_keywords, clean_titles
from .inverted_index import InvertedIndex
from .search_utils import load_movies, keyword_in_words
from models.movies_model import MoviesData

def keyword_search(search_string: str, max_results: int) -> MoviesData:

    movies_data = load_movies()
    found_movies_ids: list[int] = []
    found_movies = MoviesData()
    keywords = clean_keywords(search_string)

    movie_index = InvertedIndex()

    for word in keywords:
        for movie_id in movie_index.get_documents(word):
            found_movies_ids.append(movie_id)
            if len(found_movies_ids) >= max_results:
                break
        if len(found_movies_ids) >= max_results:
            break

    for movie_id in found_movies_ids:
        found_movies.movies.append(movie_index.get_movie(movie_id))

    found_movies.movies = sorted(found_movies.movies, key=lambda movie: movie.id, reverse=True)
    return found_movies