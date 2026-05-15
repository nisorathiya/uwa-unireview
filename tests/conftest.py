"""
Shared pytest fixtures for unit tests.
Provides a test app and client with an isolated in-memory database.
"""
import pytest
from app import create_app, db
from app.models import User, Unit
from config import TestConfig
from werkzeug.security import generate_password_hash


@pytest.fixture
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        db.session.add_all([
            Unit(code='CITS3403', name='Agile Web Development',
                 faculty='Engineering & Computing', credit_points=6),
            Unit(code='PSYC1101', name='Introduction to Psychology',
                 faculty='Science', credit_points=6),
        ])
        db.session.commit()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def test_user(app):
    with app.app_context():
        user = User(
            username='testuser',
            email='testuser@student.uwa.edu.au',
            password_hash=generate_password_hash('password123')
        )
        db.session.add(user)
        db.session.commit()
        return user


@pytest.fixture
def auth_client(client, test_user):
    client.post('/login', data={
        'email': 'testuser@student.uwa.edu.au',
        'password': 'password123'
    })
    return client
