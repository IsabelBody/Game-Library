from sqlalchemy import select, inspect

from games.adapters.orm import metadata


def test_database_populate_inspect_table_names(database_engine):

    inspector = inspect(database_engine)
    assert inspector.get_table_names(
    ) == ['games', 'games_genres', 'genres', 'publishers', 'reviews',   'users', 'wishlist', 'wishlist_games']


def test_database_populate_select_all_games(database_engine):

    inspector = inspect(database_engine)
    name_of_games_table = inspector.get_table_names()[0]

    with database_engine.connect() as connection:
        select_statement = select([metadata.tables[name_of_games_table]])
        result = connection.execute(select_statement)
        all_games = []
        for row in result:
            all_games.append(
                (row['id'], row['title'], row['price'], row['release_date'], row['description'], row['image_url'], row['website_url'], row['publisher_name']))

        nr_games = len(all_games)
        assert nr_games == 9
        assert all_games[0][0] == 7940


def test_database_populate_select_all_publishers(database_engine):

    # Get table names
    inspector = inspect(database_engine)
    name_of_publishers_table = inspector.get_table_names()[3]

    with database_engine.connect() as connection:
        # Query for records in table publishers
        select_statement = select([metadata.tables[name_of_publishers_table]])
        result = connection.execute(select_statement)

        all_publishers = []
        for row in result:
            all_publishers.append(row['name'])

        assert len(all_publishers) == 9
        assert "Ludosity" in all_publishers


def test_database_populate_select_all_genres_table(database_engine):
    # Get table names
    inspector = inspect(database_engine)

    name_of_genres_table = inspector.get_table_names()[2]
    print(name_of_genres_table)
    # replace with accurate table number for genres_table

    with database_engine.connect() as connection:
        # Query for records in table genres_table
        select_statement = select(
            [metadata.tables[name_of_genres_table]])
        result = connection.execute(select_statement)

        all_genres_table = []
        for row in result:

            all_genres_table.append(
                (row['genre_name']))

        assert len(all_genres_table) == 1
        assert all_genres_table == ['Action']


def test_database_populate_select_all_review_table(database_engine):
    # Get table names
    inspector = inspect(database_engine)
    name_of_review_table = inspector.get_table_names()[4]

    with database_engine.connect() as connection:
        # Query for records in table review_table
        select_statement = select(
            [metadata.tables[name_of_review_table]])
        result = connection.execute(select_statement)

        all_review_table = []
        for row in result:
            all_review_table.append(
                (row['id'], row['game_id'], row['user_id'], row['rating'], row['comment']))

        assert len(all_review_table) == 0
        assert all_review_table == []


def test_database_populate_select_all_users_table(database_engine):

    # Get table names
    inspector = inspect(database_engine)
    name_of_users_table = inspector.get_table_names()[5]

    with database_engine.connect() as connection:
        # Query for records in table users_table
        select_statement = select([metadata.tables[name_of_users_table]])
        result = connection.execute(select_statement)

        users = [row for row in result]
        all_users = []
        for row in result:

            all_users.append(
                (row['user_name']))

        nr_users = len(all_users)

        assert nr_users == 0
        assert all_users == []


def test_database_populate_select_all_wishlist_table(database_engine):

    # Get table names
    inspector = inspect(database_engine)
    name_of_wishlist_table = inspector.get_table_names()[6]

    with database_engine.connect() as connection:
        # Query for records in table wishlist_table
        select_statement = select(
            [metadata.tables[name_of_wishlist_table]])
        result = connection.execute(select_statement)

        all_wishlist_table = []
        for row in result:
            all_wishlist_table.append(
                (row['id'], row['wishlist_id'], row['game_id']))

        nr_wishlists = len(all_wishlist_table)

        assert nr_wishlists == 0
        assert all_wishlist_table == []


def test_database_populate_select_all_wishlist_games_table(database_engine):

    # Get table names
    inspector = inspect(database_engine)
    name_of_wishlist_games_table = inspector.get_table_names()[7]

    with database_engine.connect() as connection:
        # Query for records in table wishlist_table
        select_statement = select(
            [metadata.tables[name_of_wishlist_games_table]])
        result = connection.execute(select_statement)

        all_wishlist_table = []
        for row in result:
            all_wishlist_table.append(
                (row['id'], row['wishlist_id'], row['game_id']))

        nr_wishlist_games = len(all_wishlist_table)
        assert nr_wishlist_games == 0
        assert all_wishlist_table == []
