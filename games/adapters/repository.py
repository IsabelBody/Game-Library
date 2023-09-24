import abc
from typing import List
from games.domainmodel.model import Game, User, Publisher, Wishlist
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

    # Wishlist Methods
    @abc.abstractmethod
    def add_wishlist(self, user: User):
        raise NotImplementedError

    @abc.abstractmethod
    def add_wishlist_game(self, user: User, game: Game):
        raise NotImplementedError

    @abc.abstractmethod
    def remove_wishlist_game(self, user: User, game: Game):
        raise NotImplementedError

    @abc.abstractmethod
    def get_wishlist_games(self) -> List[Game]:
        raise NotImplementedError

    @abc.abstractmethod
    def add_game(self, game: Game):
        raise NotImplementedError

    @abc.abstractmethod
    def get_game(self, game_id) -> Game:
        raise NotImplementedError

    @abc.abstractmethod
    def get_games(self) -> List[Game]:
        raise NotImplementedError

    @abc.abstractmethod
    def add_genre(self, genre: Genre):
        raise NotImplementedError

    def get_game(self, game_id) -> Game:
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

    @abc.abstractmethod
    def add_review_to_game(self, game_id, review):
        pass

    @abc.abstractmethod
    def add_publisher(self, publisher: Publisher):
        raise NotImplementedError

    @abc.abstractmethod
    def get_publishers(self) -> List[Publisher]:
        raise NotImplementedError
