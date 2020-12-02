import os
import pytest
from main import app, db


@pytest.fixture
def client():
    app.config['TESTING'] = True
    os.environ["DATABASE_URL"] = "sqlite:///:memory:"
    client = app.test_client()

    cleanup()  # clean up before every test

    db.create_all()

    yield client

    # test1
def test_index_not_logged_in(client):
    response = client.get('/')
    assert b'Tvoje ime' in response.data

    # test2
def test_index_user_logged_in(client):
    response = client.get('/')
    assert b'stevilo 1-10' in response.data


    # test3
def test_index_logged_in(client):
    client.post('/login', data={"user-name": "Test User", "user-email": "test@user.com",
                                "user-password": "password123"}, follow_redirects=True)

    response = client.get('/')
    assert b'stevilo 1-10' in response.data


def cleanup():
    # clean up/delete the DB (drop all tables in the database)
    db.drop_all()