from sqlalchemy import select, inspect

from games.adapters.orm import metadata


def test_database_populate_inspect_table_names(database_engine):

    inspector = inspect(database_engine)
    assert inspector.get_table_names(
    ) == ['games', 'games_genres', 'genres', 'publishers', 'reviews',   'users', 'wishlist', 'wishlist_games']


def test_database_populate_select_all_games(database_engine):

    inspector = inspect(database_engine)
    name_of_games_table = inspector.get_table_names()[0]
    print(name_of_games_table)

    with database_engine.connect() as connection:
        select_statement = select([metadata.tables[name_of_games_table]])
        result = connection.execute(select_statement)
        print(result)
        all_games = []
        for row in result:
            all_games.append(
                (row['id'], row['title'], row['price'], row['release_date'], row['description'], row['image_url'], row['website_url'], row['publisher_name']))

        nr_games = len(all_games)
        assert nr_games == 5

        assert all_games == [()]


def test_database_populate_select_all_publishers(database_engine):

    # Get table names
    inspector = inspect(database_engine)
    name_of_publishers_table = inspector.get_table_names()[0]

    with database_engine.connect() as connection:
        # Query for records in table publishers
        select_statement = select([metadata.tables[name_of_publishers_table]])
        result = connection.execute(select_statement)

        all_publishers = []
        for row in result:
            all_publishers.append(row['name'])

        assert all_publishers == [()]


def test_database_populate_select_all_genres_table(database_engine):
    # Get table names
    inspector = inspect(database_engine)
    print("inspector: ", inspector)
    name_of_genres_table_table = inspector.get_table_names()[3]
    # replace with accurate table number for genres_table

    with database_engine.connect() as connection:
        # Query for records in table genres_table
        select_statement = select(
            [metadata.tables['genres']])
        result = connection.execute(select_statement)

        genres = [row for row in result]
        print(result)
        all_genres_table = []
        for row in result:
            print("should wokr")
            all_genres_table.append(
                (row['id'], row['game_id'], row['genre_name']))

        assert all_genres_table == [()]


def test_database_populate_select_all_review_table(database_engine):
    # Get table names
    inspector = inspect(database_engine)
    name_of_review_table_table = inspector.get_table_names()[1]
    # replace with accurate table number for review_table

    with database_engine.connect() as connection:
        # Query for records in table review_table
        select_statement = select(
            [metadata.tables[name_of_review_table_table]])
        result = connection.execute(select_statement)

        all_review_table = []
        for row in result:
            all_review_table.append(
                (row['id'], row['game_id'], row['user_id'], row['rating'], row['comment']))

        assert all_review_table == [()]


def test_database_populate_select_all_users_table(database_engine):

    # Get table names
    inspector = inspect(database_engine)
    name_of_users_table = inspector.get_table_names()[5]
    # print(name_of_users_table)

    with database_engine.connect() as connection:
        # Query for records in table users_table
        select_statement = select([metadata.tables['users']])
        result = connection.execute(select_statement)

        users = [row for row in result]
        print("users: ", users)
        all_users = []
        for row in result:
            # print("made it here ")
            # print(row)
            all_users.append(
                (row['user_name']))

        # print(all_users)
        nr_users = len(all_users)
        assert nr_users == 5

        # assert all_users_table[0] == [()]


def test_database_populate_select_all_wishlist_table(database_engine):

    # Get table names
    inspector = inspect(database_engine)
    name_of_wishlist_table_table = inspector.get_table_names()[1]
    # replace with accurate table number for wishlist_table

    with database_engine.connect() as connection:
        # Query for records in table wishlist_table
        select_statement = select(
            [metadata.tables[name_of_wishlist_table_table]])
        result = connection.execute(select_statement)

        all_wishlist_table = []
        for row in result:
            all_wishlist_table.append(
                (row['id'], row['wishlist_id'], row['game_id']))

        nr_users = len(all_wishlist_table)
        assert nr_users == 5

        assert all_wishlist_table[0] == [()]
