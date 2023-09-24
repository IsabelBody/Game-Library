import pytest

from flask import session


def test_register(client):
    # Check that we retrieve the register page.
    response_code = client.get('/authentication/register').status_code
    assert response_code == 200

    # Check that we can register a user successfully, supplying a valid username and password.
    response = client.post(
        '/authentication/register',
        data={'user_name': 'gmichael', 'password': 'CarelessWhisper1984'}
    )
    assert response.headers['Location'].endswith('authentication/login')


# parametrize lets us do multiple tests.
@pytest.mark.parametrize(('user_name', 'password', 'message'), (
    ('', '', b'Your user name is required'),
    ('cj', '', b'Your user name is too short'),
    ('test', '', b'Your password is required'),
    ('test', 'test', b'Your password must be at least 8 characters, and contain an upper case letter,\
            a lower case letter and a digit'),
    # this line makes it pass when it should'nt.
    ('fmercury', 'Test#6^0', b'Your user name is already taken - please supply another'),
))
def test_register_with_invalid_input(client, user_name, password, message):
    # Check that attempting to register with invalid combinations of user name and password generate appropriate error
    # messages.
    response = client.post(
        '/authentication/register',
        data={'user_name': user_name, 'password': password}
    )
    assert response.status_code == 200  # should fail to redirect
    assert message in response.data


# test register when the username is already there.
def test_register_already_exists(client):
    # When registering when someone has taken your username it should fail.
    response = client.post(
        '/authentication/register',
        data={'user_name': 'fmercury', 'password': 'Test#6^0'}
    )
    response = client.post(
        '/authentication/register',
        data={'user_name': 'fmercury', 'password': 'Test#6^0'}
    )
    assert response.status_code == 200  # should fail to redirect
    assert b'Your user name is already taken - please supply another' in response.data


def test_login(client, auth):
    # registering a user
    response_code = client.get('/authentication/register').status_code

    username = 'thorke'
    password = 'cLQ^C#oFXloS7'
    response = client.post(
        '/authentication/register',
        data={'user_name': username, 'password': password}
    )

    # Check that we can retrieve the login page.
    status_code = client.get('/authentication/login').status_code
    assert status_code == 200

    # Check that a successful login generates a redirect to the homepage.
    response = client.post(
        '/authentication/login',
        data={'user_name': username, 'password': password}
    )
    assert response.status_code == 302  # code for redirection.
    # it has to be 302 because we are redirecting.

    # Check that a session has been created for the logged-in user.
    with client:
        with client.session_transaction() as session:
            client.get('/')
            assert session['user_name'] == 'thorke'


def test_logout(client, auth):
    # Login a user.
    auth.login()

    with client:
        # Check that logging out clears the user's session.
        auth.logout()
        assert 'user_id' not in session


def test_index(client):
    # Check that we can retrieve the home page.
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome to Saveer's Arcade" in response.data


def test_end_to_end_adding_games_to_wishlist(client, auth):
    username = 'thorke'
    password = 'cLQ^C#oFXloS7'
    # registering a user
    response = client.post(
        '/authentication/register',
        data={'user_name': username, 'password': password}
    )
    # Check for successful registration and redirection
    assert response.status_code == 302

    response = client.post(
        '/authentication/login',
        data={'user_name': username, 'password': password}
    )
    assert response.status_code == 302  # code for redirection.

    response = client.get('/profile')
    assert response.status_code == 200  # Check profile page is accessible

    # Game to add to the wishlist
    game_id = 435790

    # Add game to the wishlist
    response = client.get(f'/wishlist?game_id={game_id}')
    # Check for successful addition and redirection
    assert response.status_code == 302

    # Check game is in wishlist
    response = client.get('/profile')
    assert response.status_code == 200  # Check profile page is accessible

    assert b"10 Second Ninja X has been added to your wishlist" in response.data

    auth.logout()


def test_end_to_end_removing_game_from_wishlist(client, auth):
    username = 'thorke'
    password = 'cLQ^C#oFXloS7'

    # Register a new user
    response = client.post(
        '/authentication/register',
        data={'user_name': username, 'password': password}
    )
    # Check for successful registration and redirection
    assert response.status_code == 302

    # Log in user
    response = client.post(
        '/authentication/login',
        data={'user_name': username, 'password': password}
    )
    assert response.status_code == 302  # Check for successful login and redirection

    # Access profile
    response = client.get('/profile')
    assert response.status_code == 200  # Check profile page is accessible

    # Game to add
    game_id = 435790

    # Add game to wishlist
    response = client.get(f'/wishlist?game_id={game_id}')
    # Check for successful addition and redirection
    assert response.status_code == 302

    # Check game is in wishlist
    response = client.get('/profile')
    assert response.status_code == 200  # Check that the profile page is accessible
    assert b"10 Second Ninja X" in response.data

    # Remove the game
    response = client.get(f'/remove_from_wishlist?game_id={game_id}')
    assert response.status_code == 302  # Check for successful removal and redirection

    # Check game is removed
    response = client.get('/profile')  # Access the profile page again
    assert response.status_code == 200  # Check that the profile page is accessible

    # Check game removed message
    assert b"10 Second Ninja X has been removed from your wishlist." in response.data

    auth.logout()
