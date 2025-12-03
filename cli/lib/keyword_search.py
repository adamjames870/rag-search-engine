
from .clean_keywords import clean_keywords, clean_titles
from .inverted_index import InvertedIndex
from models.movies_model import MoviesData, MovieScore


def keyword_search(search_string: str, max_results: int) -> MoviesData:

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

def bm25_search(search_string: str, max_results: int) -> list[MovieScore]:

    results = []

    movie_index = InvertedIndex()
    found_movies = movie_index.bm25_search(search_string, max_results)


    for movie_id, movie_score in found_movies.items():
        movie = movie_index.get_movie(movie_id)
        movie_score = MovieScore(id=movie_id, title=movie.title, score=movie_score)
        results.append(movie_score)

    return results


