from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Date, DateTime,
    ForeignKey
)
from sqlalchemy.orm import mapper, relationship, synonym
from games.domainmodel import model

metadata = MetaData()

users_table = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_name', String(255), unique=True, nullable=False),
    Column('password', String(255), nullable=False)
)

publishers_table = Table(
    'publishers', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(255), nullable=False)
)

games_table = Table(
    'games', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('title', String(255), unique=True, nullable=False),
    Column('price', Integer, nullable=False),
    Column('release_date', Date, nullable=False),
    Column('description', String, nullable = False),
    Column('image_url', String, nullable = False),
    Column('website_url', String, nullable = False),
    Column('publisher_id', ForeignKey('publishers.id'))
    )

genre_table = Table(
    'genres', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(255), unique=True, nullable=False),
)

games_genres_table = Table (
    'games_genres', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('game_id', ForeignKey('games.id')),
    Column('genre_id', ForeignKey('genres.id'))
)

review_table = Table(
    'reviews', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('game_id', ForeignKey('games.id')),
    Column('user_id', ForeignKey('users.id')),
    Column('rating', Integer, nullable=False),
    Column('comment',String(1000), nullable=False),
)

wishlist_table = Table (
    'wishlist', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey('users.id')),
)

wishlist_games_table = Table (
    'wishlist_games', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('wishlist_id', ForeignKey('wishlist.id')),
    Column('game_id', ForeignKey('games.id')),
)


def map_model_to_tables():
    #relationship model
    mapper(model.User, users_table, properties={
        '_User__username': users_table.c.user_name,
        '_User__password': users_table.c.password,
        '_User__reviews': relationship(model.Review, back_populates='_Review__user'),
        'User__favorite_games': relationship(model.Wishlist, back_populates="_Wishlist__list_of_games")
    })

    # relationships modelling
    mapper(model.Game, games_table, properties={
        '_Game__game_id': games_table.c.id,
        '_Game__game_title': games_table.c.title,
        '_Game__price': games_table.c.price,
        '_Game__release_date': games_table.c.release_date,
        '_Game__description':games_table.c.description,
        '_Game__image_url': games_table.c.image_url,
        '_Game__website_url': games_table.c.website_url,
        '_Game__publisher': relationship(model.Publisher),
        '_Game__genres': relationship(model.Genre, secondary=games_genres_table, back_populates='_Genre__games'),
        '_Game__reviews': relationship(model.Review, backref="_Review__user"),
        '_Game__wishlist': relationship(model.Wishlist, secondary=wishlist_games_table, back_populates='_Wishlist__games')
    })

    #relationship model
    mapper(model.Publisher, publishers_table, properties={
        '_Publisher__publisher_name': publishers_table.c.name,
        '_Publisher__games': relationship(model.Game, back_populates='_Game__publisher')
    })

    # relationship model
    mapper(model.Publisher, publishers_table, properties={
        '_Publisher__publisher_name': publishers_table.c.name
    })

    # relationship model
    mapper(model.Genre, genre_table, properties={
        '_Genre__genre_name': genre_table.c.name,
        '_Genre__games': relationship(model.Game, secondary=games_genres_table, back_populates='_Genre__genres')
    })

    mapper(model.Review, review_table, properties={
        '_Review__rating': review_table.c.rating,
        '_Review__comment': review_table.c.comment,
        '_Review__user': relationship(model.User),
        '_Review__game': relationship(model.Game)
    })

    mapper(model.Wishlist, wishlist_table, properties={
        '_Wishlist__user': relationship(model.User),
        '_Wishlist__games': relationship(model.Game, secondary=wishlist_games_table, back_populates='_Game__wishlist')
    })



