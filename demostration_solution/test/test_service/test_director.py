from unittest.mock import MagicMock
import pytest
from demostration_solution.dao.model.director import Director
from demostration_solution.dao.director import DirectorDAO
from demostration_solution.service.director import DirectorService
from demostration_solution.setup_db import db


@pytest.fixture()
def director_dao():
    director_dao = DirectorDAO(db.session)

    anton = Director(id=1, name='anton')
    sergei = Director(id=2, name='sergei')
    georgiy = Director(id=3, name='georgiy')

    director_dao.get_one = MagicMock(return_value=anton)
    director_dao.get_all = MagicMock(return_value=[anton, sergei, georgiy])
    director_dao.create = MagicMock(return_value=Director(id=3, name='semen'))
    director_dao.delete = MagicMock()
    director_dao.update = MagicMock()

    return director_dao


class TestDirectorService:

    @pytest.fixture(autouse=True)
    def director_service(self, director_dao):
        self.director_service = DirectorService(dao=director_dao)

    def test_get_one(self):
        director = self.director_service.get_one(1)
        assert director is not None
        assert director.id == 1

    def test_get_all(self):
        directors = self.director_service.get_all()
        assert len(directors) == 3
        assert len(directors) > 0

    def test_create(self):
        director_data = {
            'name': 'semen'
        }

        director = self.director_service.create(director_data)
        assert director.name == director.dao['name']

    def test_delete(self):
        director = self.director_service.delete(1)
        assert director is None

    def test_update(self):
        director_data = {'id': 3, 'name': 'artur'}
        self.director_service.update(director_data)
