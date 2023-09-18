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
        ('fmercury', 'Test#6^0', b'Your user name is already taken - please supply another'), # this line makes it pass when it should'nt.
))
def test_register_with_invalid_input(client, user_name, password, message):
    # Check that attempting to register with invalid combinations of user name and password generate appropriate error
    # messages.

    response = client.post(
        '/authentication/register',
        data={'user_name': user_name, 'password': password}
    )
    assert response.status_code == 200 # should fail to redirect
    assert message in response.data


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
    assert response.status_code == 302 # code for redirection.
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