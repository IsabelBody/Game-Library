import abc
from typing import List
from games.domainmodel.model import Game
from games.domainmodel.model import Genre

repo_instance = None

class RepositoryException(Exception):
    def __init__(self, message=None):
        print(f"repositoryException: {message}")

class AbstractRepository(abc.ABC):
    # We don't implement, because this is
    # supposed to be abstract.
    @abc.abstractmethod
    def add_game(self, game: Game):
        raise NotImplementedError

    @abc.abstractmethod
    def get_games(self) -> List[Game]:
        raise NotImplementedError

    @abc.abstractmethod
    def add_genre(self, genre: Genre):
        raise NotImplementedError

    @abc.abstractmethod
    def get_genre(self) -> List[Genre]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_games(self):
        raise NotImplementedError