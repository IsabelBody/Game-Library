import abc
from typing import List
from games.domainmodel.model import Game, User
from games.domainmodel.model import Genre

repo_instance = None

class RepositoryException(Exception):
    def __init__(self, message=None):
        print(f"repositoryException: {message}")

class AbstractRepository(abc.ABC):
    # We don't implement, because this is
    # supposed to be abstract.

    # registering user method
    @abc.abstractmethod
    def add_user(self, user: User):
        """" Adds a User to the repository. """
        raise NotImplementedError

    # login user method
    @abc.abstractmethod
    def get_user(self, user_name) -> User:
        """ Returns the User named user_name from the repository.

        If there is no User with the given user_name, this method returns None.
        """
        raise NotImplementedError

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
    def get_games_for_genre(self, genre_name) -> List[Game]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_games(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_unique_genres(self):
        raise NotImplementedError
