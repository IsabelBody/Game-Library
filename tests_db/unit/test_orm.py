# import pytest

# from sqlalchemy.exc import IntegrityError
# from games.domainmodel.model import Game, Publisher, Genre, User, Review, Wishlist

# # User test cases


# def make_user():
#     user = User("hasan", "Password123")
#     return user


# def insert_user(empty_session, values=None):
#     new_name = 'hasan'
#     new_password = 'Password123'

#     if values is not None:
#         new_name = values[0]
#         new_password = values[1]

#     empty_session.execute("INSERT INTO users (user_name, password) VALUES (:user_name, :password)",
#                           {'user_name': new_name, 'password': new_password})

#     row = empty_session.execute('SELECT id from users where user_name = :user_name',
#                                 {'user_name': new_name}).fetchone()

#     return row[0]


# def insert_users(empty_session, values):
#     for value in values:
#         empty_session.execute('INSERT INTO users (user_name, password) VALUES (:user_name, :password)',
#                               {'user_name': value[0], 'password': value[1]})
#     rows = list(empty_session.execute('SELECT id from users'))
#     keys = tuple(row[0] for row in rows)
#     return keys


# def test_saving_users(empty_session):
#     user = make_user()
#     empty_session.add(user)
#     empty_session.commit()

#     rows = list(empty_session.execute('SELECT user_name, password FROM users'))
#     assert rows == [("hasan", "Password123")]


# def test_loading_users(empty_session):
#     users = list()
#     users.append(("hasan", "Password123"))
#     users.append(("jason", "Laptop123"))
#     insert_users(empty_session, users)

#     expected = [User("hasan", "Password123"), User("jason", "Laptop123")]

#     assert empty_session.query(User).all() == expected


# def test_saving_users_with_common_user_name(empty_session):
#     insert_user(empty_session, ("hasan", "Password123"))
#     empty_session.commit()

#     with pytest.raises(IntegrityError):
#         user = User("hasan", "AnotherPassword")
#         empty_session.add(user)
#         empty_session.commit()

# # # Game Test Cases


# def make_game():
#     game = Game(1, "SaveerGame")
#     game.price = 10.0
#     game.release_date = "Oct 21, 2008"
#     game.description = "A fun game"
#     game.image_url = "saveer_image.jpg"
#     game.website_url = "https://saveer-game.com"
#     return game


# def insert_game(empty_session):
#     empty_session.execute(
#         'INSERT INTO games (title, price, release_date, description, image_url, website_url) VALUES'
#         '("Saveers game", :price, "Oct 21, 2008", "A fun game", "saveer_image.jpg", "https://saveer-game.com")',
#         {'price': 10.0}
#     )
#     row = empty_session.execute(
#         'SELECT id from games where title = "Saveers game"').fetchone()

#     return row[0]


# def insert_games(empty_session, values):
#     for value in values:
#         empty_session.execute(
#             'INSERT INTO games (title, price, release_date, description, image_url, website_url) VALUES'
#             '(:title, :price, :release_date, :description, ":image_url, :website_url)',
#             {'title': value.title, 'price': 10.0, 'release_date': value.release_date,
#                 'description': value.description, 'image_url': value.image_url, 'website_url': value.website_url}
#         )


# def insert_game_genre_associations(empty_session, game_key, genre_names):
#     stmt = 'INSERT INTO games_genres (game_id, genre_name) VALUES (:game_id, :genre_name)'
#     for genre_name in genre_names:
#         empty_session.execute(
#             stmt, {'game_id': game_key, 'genre_name': genre_name})


# def insert_game_wishlist_associations(empty_session, game_keys, wishlist_id):
#     stmt = 'INSERT INTO wishlist_games (wishlist_id, game_id) VALUES (:wishlist_id, :game_id)'
#     for game_id in game_keys:
#         empty_session.execute(
#             stmt, {'wishlist_id': wishlist_id, 'game_id': game_id})


# def insert_reviewed_game(empty_session):
#     game_id = insert_game(empty_session)
#     user_id = insert_user(empty_session)

#     empty_session.execute("INSERT INTO reviews (game_id, user_id, rating, comment) VALUES (:game_id, :user_id, :rating, 'Comment 1')",
#                           {'game_id': game_id, 'user_id': user_id, 'rating': 5})
#     row = empty_session.execute('SELECT id from reviews where comment = :comment',
#                                 {'comment': "Comment 1"}).fetchone()

#     return row[0]


# def test_loading_of_game(empty_session):
#     game_key = insert_game(empty_session)
#     expected_game = make_game()
#     fetched_game = empty_session.query(Game).one()

#     assert expected_game == fetched_game
#     assert game_key == fetched_game.game_id


# def test_loading_of_reviewed_game(empty_session):
#     insert_reviewed_game(empty_session)

#     rows = empty_session.query(Game).all()
#     game = rows[0]

#     for review in game.reviews:
#         assert review.game is game


# def test_loading_of_game_genres(empty_session):
#     game_id = insert_game(empty_session)
#     genreNames = insert_genres(
#         empty_session, ['saveerAnime', 'hasanAnime', 'jasonAnime'])
#     insert_game_genre_associations(empty_session, game_id, genreNames)

#     game = empty_session.query(Game).get(game_id)
#     genres = [empty_session.query(Genre).get(genre) for genre in genreNames]

#     for genre in genres:
#         assert genre in game.genres


# def test_saving_of_game(empty_session):
#     game = make_game()
#     empty_session.add(game)
#     empty_session.commit()

#     rows = list(empty_session.execute(
#         'SELECT title, price, release_date, description, image_url, website_url FROM games'))

#     assert rows == [("SaveerGame", 10.0, "Oct 21, 2008", "A fun game",
#                      "saveer_image.jpg", "https://saveer-game.com")]


# def test_saving_and_loading_game(empty_session):
#     game = make_game()
#     empty_session.add(game)
#     empty_session.commit()

#     loaded_game = empty_session.query(Game).first()
#     assert loaded_game.title == "SaveerGame"
#     assert loaded_game.price == 10.0
#     assert loaded_game.release_date == "Oct 21, 2008"
#     assert loaded_game.description == "A fun game"
#     assert loaded_game.image_url == "saveer_image.jpg"
#     assert loaded_game.website_url == "https://saveer-game.com"

# # # Publisher test cases


# def make_publisher():
#     publisher = Publisher("saveerPublishing")
#     return publisher


# def insert_publisher(empty_session, value=None):
#     new_name = 'HasanPublishing'

#     if value is not None:
#         new_name = value

#     empty_session.execute("INSERT INTO publishers (name) VALUES (:name)",
#                           {'name': new_name})
#     row = empty_session.execute('SELECT name from publishers where name = (:name)',
#                                 {'name': new_name}).fetchone()

#     return row[0]


# def insert_publishers(empty_session, values):
#     for value in values:
#         empty_session.execute('INSERT INTO publishers (name) VALUES (:name)',
#                               {'name': value})
#     rows = list(empty_session.execute('SELECT name from publishers'))
#     keys = tuple(row[0] for row in rows)
#     return keys


# def test_saving_publishers(empty_session):
#     publisher = make_publisher()
#     empty_session.add(publisher)
#     empty_session.commit()

#     rows = list(empty_session.execute('SELECT name FROM publishers'))
#     assert rows[0][0] == "saveerPublishing"


# def test_loading_publishers(empty_session):
#     publishers = list()
#     publishers.append(("saveerPublishing"))
#     publishers.append(("hasanPublishing"))
#     insert_publishers(empty_session, publishers)

#     expected = [Publisher("saveerPublishing"),
#                 Publisher("hasanPublishing")]

#     assert empty_session.query(Publisher).all() == expected


# def test_saving_publishers_with_common_name(empty_session):
#     insert_publisher(empty_session, ("saveerPublishing"))
#     empty_session.commit()

#     with pytest.raises(IntegrityError):
#         publisher = Publisher("saveerPublishing",)
#         empty_session.add(publisher)
#         empty_session.commit()

# # Game genres test cases


# def make_genre():
#     genre = Genre("AnimeHasan")
#     return genre


# def insert_genre(empty_session, value=None):
#     new_name = 'AnimeHasan'

#     if value is not None:
#         new_name = value

#     empty_session.execute("INSERT INTO genres (genre_name) VALUES (:genre_name)",
#                           {'genre_name': new_name})
#     row = empty_session.execute('SELECT genre_name from genres')

#     return row


# def insert_genres(empty_session, values):
#     for value in values:
#         empty_session.execute('INSERT INTO genres (genre_name) VALUES (:genre_name)',
#                               {'genre_name': value})
#     rows = list(empty_session.execute('SELECT genre_name from genres'))
#     keys = tuple(row[0] for row in rows)
#     return keys


# def test_saving_genres(empty_session):
#     genre = make_genre()

#     empty_session.add(genre)
#     empty_session.commit()

#     rows = list(empty_session.execute('SELECT genre_name FROM genres'))
#     assert rows[0][0] == "AnimeHasan"


# def test_loading_genres(empty_session):
#     genres = list()
#     genres.append(("AnimeHasan"))
#     genres.append(("AnimeJason"))
#     insert_genres(empty_session, genres)

#     expected = [Genre("AnimeHasan"),
#                 Genre("AnimeJason")]

#     assert empty_session.query(Genre).all() == expected


# def test_saving_genres_with_common_name(empty_session):
#     insert_genre(empty_session, ("AnimeHasan"))
#     empty_session.commit()

#     with pytest.raises(IntegrityError):
#         genre = Genre("AnimeHasan")
#         empty_session.add(genre)
#         empty_session.commit()

# # # Reviews test cases


# def make_review(user: User, game: Game, rating: int, comment_text: str,):
#     user = User("hasan", "Password123")
#     game = Game(1234, "hasan's Game")
#     review = Review(user, game, rating, comment_text)

#     user.add_review(review)
#     game.add_review(review)
#     return review


# def insert_review(empty_session):
#     game_key = insert_game(empty_session)
#     user_key = insert_user(empty_session)

#     empty_session.execute("INSERT INTO reviews (game_id, user_id, rating, comment) VALUES (:game_id, :user_id, :rating, 'Comment 1')",
#                           {'game_id': game_key, 'user_id': user_key, 'rating': 5})
#     row = empty_session.execute('SELECT id from reviews where comment = :comment',
#                                 {'comment': "Comment 1"}).fetchone()
#     # might have to modify to get more accurate code
#     return row[0]


# def test_loading_of_review(empty_session):
#     insert_review(empty_session)

#     rows = empty_session.query(Review).all()

#     expected = "Comment 1"

#     assert rows[0].comment == expected


# # def test_saving_reviews(empty_session):

# #     game_key = insert_game(empty_session)
# #     user_key = insert_user(empty_session)

# #     game = empty_session.query(Game).filter(
# #         Game._Game__game_title == 'HasanGame').one()
# #     user = empty_session.query(User).filter(
# #         User._User__username == 'hasan').one()

# #     comment = "Im loving it"
# #     rating = 5
# #     review = make_review(user, game, rating, comment)

# #     empty_session.add(review)
# #     empty_session.commit()

# #     rows = list(empty_session.execute(
# #         'SELECT user_id, game_id, rating, comment FROM reviews'))

# #     assert rows == [(user_key, game_key, rating, comment)]

# # # Wishlist test cases


# def make_wishlist(empty_session):
#     user = insert_user(empty_session)
#     wishlist = Wishlist(user)
#     return wishlist


# def insert_wishlist(empty_session):
#     user_key = insert_user(empty_session)

#     empty_session.execute("INSERT INTO wishlist (user_id) VALUES (:user_id)",
#                           {'user_id': user_key})
#     row = empty_session.execute('SELECT user_id from wishlist')
#     return row


# def test_loading_of_wishlist(empty_session):
#     game = make_game()

#     insert_wishlist(empty_session)

#     rows = empty_session.query(Wishlist).all()

#     user = empty_session.execute('SELECT id from users where user_name = :user_name',
#                                  {'user_name': 'hasan'}).fetchone()

#     assert rows[0].user_id == user[0]


# # def test_loading_of_wishlist_games(empty_session):
# #     game_values = [
# #         {
# #             'title': "saveersGame",
# #             'price': 10.2,
# #             'release_date': "2023-06-25",
# #             'description': "This is saveers game.",
# #             'image_url': "saveersGame_image.jpg",
# #             'website_url': "https://saveersGame-website.com"
# #         },
# #         {
# #             'title': "hasansGame",
# #             'price': 29.99,
# #             'release_date': "2023-07-05",
# #             'description': "This is hasans game",
# #             'image_url': "hasansGame_image.jpg",
# #             'website_url': "https://hasansGame-website.com"
# #         },

# #     ]
# #     game_ids = insert_games(empty_session, game_values)
# #     wishlist_id = insert_wishlist(empty_session)
# #     insert_game_wishlist_associations(empty_session, game_ids, wishlist_id)

# #     wishlist = empty_session.query(Wishlist).get(id)
# #     games = [empty_session.query(Game).get(game_id) for game_id in game_ids]

# #     for game in games:
# #         assert game in wishlist.list_of_games()
