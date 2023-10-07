from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Text, Float, ForeignKey
)
from sqlalchemy.orm import mapper, relationship

from games.domainmodel import model

# global variable giving access to the MetaData (schema) information of the database
# global variable givin access to the MetaData (schema) information of the database
metadata = MetaData()

publishers_table = Table(
    'publishers', metadata,
    # We only want to maintain those attributes that are in our domain model
    # For publisher, we only have name.
    Column('name', String(255), primary_key=True)  # nullable=False, unique=True)
)

games_table = Table(
    'games', metadata,
    Column('id', Integer, primary_key=True),
    Column('title', Text, nullable=False),
    Column('price', Float, nullable=False),
    Column('release_date', String(50), nullable=False),
    Column('description', String(255), nullable=True),
    Column('image_url', String(255), nullable=True),
    Column('website_url', String(255), nullable=True),
    Column('publisher_name', ForeignKey('publishers.name'))
)

genres_table = Table(
    'genres', metadata,
    # For genre again we only have name.
    Column('genre_name', String(64), primary_key=True, nullable=False)
)

games_genres_table = Table(
    'games_genres', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('game_id', ForeignKey('games.id')),
    Column('genre_name', ForeignKey('genres.genre_name'))
)

review_table = Table(
    'reviews', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('game_id', ForeignKey('games.id')),
    Column('user_id', ForeignKey('users.id')),
    Column('rating', Integer, nullable=False),
    Column('comment', String(1000), nullable=False),
)

users_table = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_name', String(255), unique=True, nullable=False),
    Column('password', String(255), nullable=False)
)

wishlist_table = Table(
    'wishlist', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey('users.id')),
)

wishlist_games_table = Table(
    'wishlist_games', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('wishlist_id', ForeignKey('wishlist.id')),
    Column('game_id', ForeignKey('games.id')),
)


def map_model_to_tables():
    # Relationship model for User
    mapper(
        model.User,
        users_table,
        properties={
            '_User__username': users_table.c.user_name,
            '_User__password': users_table.c.password,
            '_User__reviews': relationship(model.Review, back_populates='_Review__user'),
            '_User__wishlist': relationship(model.Wishlist, back_populates='_Wishlist__user')
        }
    )
    # Relationship model for Game
    mapper(model.Game, games_table, properties={
        '_Game__game_id': games_table.c.id,
        '_Game__game_title': games_table.c.title,
        '_Game__price': games_table.c.price,
        '_Game__release_date': games_table.c.release_date,
        '_Game__description': games_table.c.description,
        '_Game__image_url': games_table.c.image_url,
        '_Game__website_url': games_table.c.website_url,
        '_Game__publisher': relationship(model.Publisher),
        '_Game__genres': relationship(model.Genre, secondary=games_genres_table, back_populates='_Genre__games'),
        '_Game__reviews': relationship(model.Review, back_populates="_Review__game"),
        '_Game__wishlist': relationship(model.Wishlist, secondary=wishlist_games_table, back_populates='_Wishlist__list_of_games')
    })

    # Relationship model for Publisher
    mapper(model.Publisher, publishers_table, properties={
        '_Publisher__publisher_name': publishers_table.c.name
    })

    # Relationship model for Genre
    mapper(model.Genre, genres_table, properties={
        '_Genre__genre_name': genres_table.c.genre_name,
        '_Genre__games': relationship(model.Game, secondary=games_genres_table, back_populates='_Game__genres')
    })

    # Relationship model for Review
    mapper(model.Review, review_table, properties={
        '_Review__rating': review_table.c.rating,
        '_Review__comment': review_table.c.comment,
        '_Review__user': relationship(model.User),
        '_Review__game': relationship(model.Game)
    })

    # Relationship model for Wishlist
    mapper(model.Wishlist, wishlist_table, properties={
        '_Wishlist__user': relationship(model.User),
        '_Wishlist__list_of_games': relationship(
            model.Game,
            secondary=wishlist_games_table,
            back_populates='_Game__wishlist'
        )
    })
