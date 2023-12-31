from datetime import date
from typing import List

from sqlalchemy import desc, asc
from sqlalchemy.exc import NoResultFound, MultipleResultsFound

from sqlalchemy.orm import scoped_session
from games.adapters.repository import AbstractRepository
from games.authentication.services import user_to_dict
from games.domainmodel.model import User, Game, Genre, Review, Publisher, Wishlist
from sqlalchemy.orm import joinedload


class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        # this method can be used e.g. to allow Flask to start a new session for each http request,
        # via the 'before_request' callback
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    def add_user(self, user: User):
        with self._session_cm as scm:
            scm.session.add(user)
            scm.commit()

    def add_publisher(self, publisher: Publisher):
        with self._session_cm as scm:
            scm.session.merge(publisher)
            scm.commit()

    def commit(self):
        self._session_cm.commit()

    def get_user(self, user_name: str) -> User:
        user = None
        try:
            users = self._session_cm.session.query(User).all()

            filtered_users = [
                user for user in users if user.username == user_name]
            return filtered_users[0]

        except:
            return None

    def add_game(self, game: Game):
        with self._session_cm as scm:
            scm.session.merge(game)
            scm.commit()

    def get_game(self, game_id) -> Game:
        try:
            games = self._session_cm.session.query(Game).all()
            filtered_games = [
                game for game in games if game.game_id == game_id]
            return filtered_games[0]
        except:
            return None

    def add_genre(self, genre: Genre):
        with self._session_cm as scm:
            scm.session.merge(genre)
            scm.commit()

    def get_games(self) -> List[Game]:
        games_all = self._session_cm.session.query(Game).all()
        return games_all

    def get_genre(self) -> List[Genre]:
        genres_all = self._session_cm.session.query(Genre).all()
        genres_all.sort()
        return genres_all

    def get_games_for_genre(self, genre_name) -> List[Game]:
        genre = Genre(genre_name)
        all_games = self.get_games()

        games_by_genre = []
        for game in all_games:
            if genre in game.genres:
                games_by_genre.append(game)
        return games_by_genre

    def get_number_of_games(self):
        count_games = self._session_cm.session.query(Game).count()
        return count_games

    def get_publishers(self) -> List[Publisher]:
        all_publishers = self._session_cm.session.query(Publisher).all()
        return all_publishers

    def get_number_of_unique_genres(self):
        num_unique = self._session_cm.session.query(Genre).distinct().count()
        return num_unique

    def add_wishlist(self, user: User):
        wishlists = self._session_cm.session.query(Wishlist).all()
        for wishlist in wishlists:
            if wishlist.user == user:
                return

        with self._session_cm as scm:
            wishlist = Wishlist(user)
            scm.session.add(wishlist)
            scm.commit()

    def add_wishlist_game(self, user: User, game: Game):
        with self._session_cm as scm:
            user_wishlist = self.get_wishlist_games(user)

            if user_wishlist is None:
                user_wishlist = Wishlist(user)
                scm.session.add(user_wishlist)

            user_wishlist.add_game(game)
            scm.commit()

    def remove_wishlist_game(self, user: User, game: Game):
        with self._session_cm as scm:
            user_wishlist = self.get_wishlist_games(user)
            if user_wishlist and game in user_wishlist:
                user_wishlist.remove_game(game)
                scm.commit()

    def get_wishlist_games(self, user: User) -> List[Game]:
        with self._session_cm as scm:
            wishlists = scm.session.query(Wishlist).all()
            filtered_wishlists = [
                wishlist for wishlist in wishlists if user.id == wishlist.user_id]

            user_wishlist = filtered_wishlists[0]

            if user_wishlist:
                return user_wishlist
            return []

    def add_review_to_game(self, game_id, review):
        with self._session_cm as scm:
            game = self.get_game(game_id)

            if game:
                game.reviews.append(review)
                scm.commit()

    def get_reviews_for_game(self, game_id) -> List[Review]:
        try:
            game = self.get_game(game_id)
            print(game)
            if game is not None:
                return game.reviews
            else:
                return []
        except:
            return []
