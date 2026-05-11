"""
Selenium test fixtures.
Runs a Flask server in a background thread, exposes a Chrome driver.
"""
import pytest
import threading
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from app import create_app, db
from app.models import Unit, User
from config import TestConfig
from werkzeug.security import generate_password_hash


TEST_PORT = 5555


@pytest.fixture(scope='session')
def live_server():
    app = create_app(TestConfig)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_selenium.db'

    with app.app_context():
        db.drop_all()
        db.create_all()
        db.session.add_all([
            Unit(code='CITS3403', name='Agile Web Development',
                 faculty='Engineering & Computing', credit_points=6),
            Unit(code='PSYC1101', name='Introduction to Psychology',
                 faculty='Science', credit_points=6),
        ])
        db.session.add(User(
            username='seleniumuser',
            email='seleniumuser@student.uwa.edu.au',
            password_hash=generate_password_hash('password123')
        ))
        db.session.commit()

    server = threading.Thread(
        target=lambda: app.run(port=TEST_PORT, use_reloader=False),
        daemon=True
    )
    server.start()
    time.sleep(1)

    yield f'http://localhost:{TEST_PORT}'


@pytest.fixture
def driver():
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1280,800')

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    yield driver
    driver.quit()