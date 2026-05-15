"""
Selenium WebDriver test fixtures.

These fixtures spin up a real Flask server in a background thread using
werkzeug's make_server (so it can be shut down cleanly), and expose a
headless Chrome driver per test.

The database is reset and re-seeded before every test, so tests are
fully isolated from one another — running them in any order, or
individually, produces the same result.
"""
import os
import socket
import threading
import time

import pytest
from werkzeug.serving import make_server
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from app import create_app, db
from app.models import User, Unit, Review
from config import TestConfig
from werkzeug.security import generate_password_hash


# ─── Configuration ────────────────────────────────────────────────────────
TEST_PORT = 5555

# Path for the test SQLite file. Must be file-based (not :memory:) because
# the Flask server runs in a separate thread from the test process, and
# in-memory SQLite is per-connection.
TEST_DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                            'selenium_test.db'))


class SeleniumTestConfig(TestConfig):
    """Test config with a file-based SQLite DB shared across threads."""
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{TEST_DB_PATH}'
    WTF_CSRF_ENABLED = False    # disable CSRF so Selenium can drive forms
    SERVER_NAME = None          # let Flask figure out from the request


class _ServerThread(threading.Thread):
    """A controllable Werkzeug server running in a background thread."""

    def __init__(self, app, port):
        super().__init__(daemon=True)
        self.server = make_server('127.0.0.1', port, app, threaded=True)
        self.ctx = app.app_context()
        self.ctx.push()

    def run(self):
        self.server.serve_forever()

    def shutdown(self):
        self.server.shutdown()


def _wait_for_port(host, port, timeout=5.0):
    """Block until a TCP port accepts connections (or raise)."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with socket.create_connection((host, port), timeout=0.5):
                return True
        except OSError:
            time.sleep(0.1)
    raise RuntimeError(f'Server on port {port} did not start in {timeout}s')


# ─── Session-scoped Flask app + server ────────────────────────────────────
@pytest.fixture(scope='session')
def _app():
    """Create the Flask app once per test session."""
    # Remove any stale test DB from a previous interrupted run
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)

    app = create_app(SeleniumTestConfig)

    with app.app_context():
        db.create_all()

    yield app

    if os.path.exists(TEST_DB_PATH):
        try:
            os.remove(TEST_DB_PATH)
        except OSError:
            pass


@pytest.fixture(scope='session')
def live_server(_app):
    """Start a real Werkzeug server in a background thread.

    Yields the base URL of the running server. The server is shut down
    cleanly at the end of the session.
    """
    server = _ServerThread(_app, TEST_PORT)
    server.start()
    _wait_for_port('127.0.0.1', TEST_PORT, timeout=5.0)

    yield f'http://localhost:{TEST_PORT}'

    server.shutdown()
    server.join(timeout=5.0)


# ─── Per-test database reset ──────────────────────────────────────────────
@pytest.fixture(autouse=True)
def _reset_db(_app, live_server):
    """Wipe and re-seed the database before every Selenium test.

    Runs automatically for every test in this directory so each test
    starts from the same known state — no leakage between tests.
    """
    with _app.app_context():
        db.drop_all()
        db.create_all()

        units = [
            Unit(code='CITS3403', name='Agile Web Development',
                 faculty='Engineering & Computing', credit_points=6),
            Unit(code='CITS1401', name='Computational Thinking with Python',
                 faculty='Engineering & Computing', credit_points=6),
            Unit(code='PSYC1101', name='Introduction to Psychology',
                 faculty='Science', credit_points=6),
        ]
        user = User(
            username='seleniumuser',
            email='seleniumuser@student.uwa.edu.au',
            password_hash=generate_password_hash('password123'),
        )
        db.session.add_all(units + [user])
        db.session.commit()

    yield


# ─── Chrome WebDriver ─────────────────────────────────────────────────────
@pytest.fixture
def driver():
    """Headless Chrome driver. New instance per test, quit at the end.

    Set the HEADLESS env var to '0' to watch tests run in a visible window:
        HEADLESS=0 pytest tests/selenium
    """
    options = Options()
    if os.environ.get('HEADLESS', '1') != '0':
        options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1280,900')

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options,
    )
    driver.implicitly_wait(0)   # we use explicit waits everywhere
    yield driver
    driver.quit()


# ─── Helper: log in via the browser ───────────────────────────────────────
@pytest.fixture
def logged_in_driver(driver, live_server):
    """A driver already logged in as the seeded seleniumuser."""
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    driver.get(f'{live_server}/login')
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, 'form-login'))
    )
    login_form = driver.find_element(By.ID, 'form-login')
    login_form.find_element(By.NAME, 'email').send_keys('seleniumuser@student.uwa.edu.au')
    login_form.find_element(By.NAME, 'password').send_keys('password123')
    # WTForms renders SubmitField as <input type="submit">, not <button>
    login_form.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()

    # Wait for the dashboard to load (search input is dashboard-specific)
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, 'search-input'))
    )
    return driver


# ─── Helper: seed extra data inside the test ──────────────────────────────
@pytest.fixture
def seed_helper(_app):
    """Returns helper functions tests can call to seed extra data
    (additional users, reviews, etc.) into the per-test DB."""

    def add_user(username, email, password='password123'):
        with _app.app_context():
            u = User(
                username=username,
                email=email,
                password_hash=generate_password_hash(password),
            )
            db.session.add(u)
            db.session.commit()
            return u.id

    def add_review(user_id, unit_code, overall=4, workload=3,
                   difficulty=3, usefulness=4,
                   comment='A solid unit with helpful content for students.',
                   year=2024, semester='S1'):
        with _app.app_context():
            unit = Unit.query.filter_by(code=unit_code).first()
            r = Review(
                user_id=user_id,
                unit_id=unit.id,
                overall_rating=overall,
                workload_rating=workload,
                difficulty_rating=difficulty,
                usefulness_rating=usefulness,
                comment=comment,
                year_taken=year,
                semester=semester,
            )
            db.session.add(r)
            db.session.commit()
            return r.id

    def get_user_id(username):
        with _app.app_context():
            u = User.query.filter_by(username=username).first()
            return u.id if u else None

    return type('SeedHelper', (), {
        'add_user': staticmethod(add_user),
        'add_review': staticmethod(add_review),
        'get_user_id': staticmethod(get_user_id),
    })
