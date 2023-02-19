from unittest.mock import MagicMock
import pytest
from demostration_solution.dao.model.movie import Movie
from demostration_solution.dao.movie import MovieDAO
from demostration_solution.service.movie import MovieService
from demostration_solution.setup_db import db


@pytest.fixture()
def movie_dao():
    movie_dao = MovieDAO(db.session)

    movie_1 = Movie(id=1, title='movie_1', description='description_1', trailer='trailer_1', year=2001, raiting=2,
                    genre_id=1, director_id=1)
    movie_2 = Movie(id=2, title='movie_2', description='description_2', trailer='trailer_2', year=2002, raiting=2,
                    genre_id=2, director_id=2)
    movie_3 = Movie(id=3, title='movie_3', description='description_3', trailer='trailer_2', year=2003, raiting=2,
                    genre_id=3, director_id=3)

    movie_dao.get_one = MagicMock(return_value=movie_1)
    movie_dao.get_all = MagicMock(return_value=[movie_1, movie_2, movie_3])
    movie_dao.create = MagicMock(return_value=Movie(id=3, title='movie_4'))
    movie_dao.delete = MagicMock()
    movie_dao.update = MagicMock()

    return movie_dao


class TestMovieService:

    @pytest.fixture(autouse=True)
    def movie_service(self, movie_dao):
        self.movie_service = MovieService(dao=movie_dao)

    def test_get_one(self):
        movie = self.movie_service.get_one(1)
        assert movie is not None
        assert movie.id == 1
        assert movie.title == 'movie_1'

    def test_get_all(self):
        movies = self.movie_service.get_all()
        assert len(movies) == 3
        assert len(movies) > 0

    def test_create(self):
        movie_data = {
            'title': 'movie_4'
        }

        movie = self.movie_service.create(movie_data)
        assert movie.title == movie.dao['title']

    def test_delete(self):
        movie = self.movie_service.delete(1)
        assert movie is None

    def test_update(self):
        movie_data = {'id': 3, 'title': 'movie_5'}
        self.movie_service.update(movie_data)
