"""Unit tests for authentication routes — register, login, logout."""

from app import db
from app.models import User
from werkzeug.security import check_password_hash


def test_register_with_valid_uwa_email(client, app):
    response = client.post('/register', data={
        'name': 'Alice',
        'email': 'alice@student.uwa.edu.au',
        'password': 'password123',
        'confirm': 'password123'
    }, follow_redirects=True)
    assert response.status_code == 200
    with app.app_context():
        user = User.query.filter_by(email='alice@student.uwa.edu.au').first()
        assert user is not None


def test_register_rejects_non_uwa_email(client):
    response = client.post('/register', data={
        'name': 'Bob',
        'email': 'bob@gmail.com',
        'password': 'password123',
        'confirm': 'password123'
    })
    assert b'UWA student email' in response.data


def test_register_password_is_hashed(client, app):
    client.post('/register', data={
        'name': 'Carol',
        'email': 'carol@student.uwa.edu.au',
        'password': 'mypassword',
        'confirm': 'mypassword'
    })
    with app.app_context():
        user = User.query.filter_by(email='carol@student.uwa.edu.au').first()
        assert user.password_hash != 'mypassword'
        assert check_password_hash(user.password_hash, 'mypassword')


def test_register_duplicate_email_rejected(client, test_user):
    response = client.post('/register', data={
        'name': 'Different',
        'email': 'testuser@student.uwa.edu.au',
        'password': 'password123',
        'confirm': 'password123'
    })
    assert b'already exists' in response.data


def test_login_with_correct_credentials(client, test_user):
    response = client.post('/login', data={
        'email': 'testuser@student.uwa.edu.au',
        'password': 'password123'
    }, follow_redirects=True)
    assert response.status_code == 200


def test_login_with_wrong_password(client, test_user):
    response = client.post('/login', data={
        'email': 'testuser@student.uwa.edu.au',
        'password': 'wrongpassword'
    })
    assert b'Invalid email or password' in response.data


def test_logout_clears_session(auth_client):
    response = auth_client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'You have been logged out' in response.data