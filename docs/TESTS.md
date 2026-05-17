# Testing Documentation

## Overview

UniReview uses **pytest** and **pytest-flask** for unit testing, and **Selenium WebDriver** for end-to-end browser testing. Unit tests are isolated using an in-memory SQLite database. Selenium tests run against a live Flask server with a file-based SQLite database.

---

## Technology Stack

| Component | Technology |
|-----------|------------|
| Test framework | pytest |
| Flask integration | pytest-flask |
| Unit test database | In-memory SQLite (via `TestConfig`) |
| Selenium browser | Chrome (headless by default) |
| Selenium test database | File-based SQLite (per session) |
| HTML reports | pytest-html |

---

## How to Run

### Install dependencies
```bash
pip install -r requirements.txt
```

### Run unit tests only
```bash
pytest tests/ --ignore=tests/selenium -v
```

### Run Selenium tests only
```bash
pytest tests/selenium -v
```

### Run all tests
```bash
pytest tests -v
```

### Run a single test file
```bash
pytest tests/test_auth.py -v
pytest tests/test_reviews.py -v
pytest tests/test_api_saves.py -v
pytest tests/selenium/test_user_flow.py -v
pytest tests/selenium/test_search.py -v
pytest tests/selenium/test_reviews.py -v
```

### Run Selenium tests in visible browser (non-headless)
```bash
HEADLESS=0 pytest tests/selenium -v
```

### Generate an HTML report
```bash
pytest tests/ -v --html=report.html
```
Then open `report.html` in your browser. `pytest-html` and `pytest-metadata` are included in `requirements.txt`.

---

## Test Structure

```
tests/
├── __init__.py
├── conftest.py              # shared unit test fixtures
├── test_auth.py             # authentication route tests
├── test_reviews.py          # review submit/edit/delete tests
├── test_api_saves.py        # API endpoints and saved units tests
└── selenium/
    ├── __init__.py
    ├── conftest.py          # Selenium fixtures (live server, Chrome driver)
    ├── test_user_flow.py    # register/login/logout browser tests
    ├── test_search.py       # dashboard search and filter browser tests
    └── test_reviews.py      # review submit, edit, save, upvote browser tests
```

### Shared Unit Test Fixtures (`tests/conftest.py`)

All fixtures are available to every unit test file automatically.

| Fixture | Description |
|---------|-------------|
| `app` | Creates a test Flask app with `TestConfig` — in-memory SQLite, CSRF disabled. Seeds two test units (`CITS3403`, `PSYC1101`). Tears down after each test. |
| `client` | Flask test client for unauthenticated requests. |
| `test_user` | Creates a user (`testuser@student.uwa.edu.au`) in the test DB. |
| `auth_client` | A test client already logged in as `test_user`. |

### Selenium Fixtures (`tests/selenium/conftest.py`)

| Fixture | Description |
|---------|-------------|
| `_app` | Session-scoped Flask app with file-based SQLite DB shared across threads. |
| `live_server` | Starts a real Werkzeug server on port 5555 in a background thread. Yields the base URL. |
| `_reset_db` | Auto-use fixture — wipes and re-seeds the DB before every Selenium test for full isolation. |
| `driver` | Headless Chrome WebDriver instance. New instance per test, quit at the end. |
| `logged_in_driver` | A Chrome driver already logged in as `seleniumuser`. |
| `seed_helper` | Helper functions to seed additional users and reviews inside a test. |

---

## Test Cases

### `test_auth.py` — Authentication Routes

| # | Test | Description | Expected Output |
|---|------|-------------|-----------------|
| 1 | `test_register_with_valid_uwa_email` | Register with a valid UWA student email | 200, user exists in DB |
| 2 | `test_register_rejects_non_uwa_email` | Register with a non-UWA email | Response contains "UWA student email" |
| 3 | `test_register_password_is_hashed` | Password is not stored as plain text | Stored hash differs from plain password |
| 4 | `test_register_duplicate_email_rejected` | Register with an already existing email | Response contains "already exists" |
| 5 | `test_login_with_correct_credentials` | Login with correct email and password | 200 |
| 6 | `test_login_with_wrong_password` | Login with incorrect password | Response contains "Invalid email or password" |
| 7 | `test_logout_clears_session` | Logout redirects and clears session | 200, response contains "You have been logged out" |

---

### `test_reviews.py` — Review Routes

| # | Test | Description | Expected Output |
|---|------|-------------|-----------------|
| 8 | `test_submit_review_requires_login` | Submit a review without being logged in | 302 redirect to login |
| 9 | `test_submit_review_success` | Logged in user submits a valid review | 200, review exists in DB |
| 10 | `test_submit_review_duplicate_rejected` | Submit a second review for the same unit | Duplicate rejected |
| 11 | `test_submit_review_invalid_unit` | Submit a review for a non-existent unit | 404 |
| 12 | `test_submit_review_comment_too_short` | Submit a review with comment under 20 characters | Review rejected |
| 13 | `test_submit_review_invalid_rating` | Submit a review with rating outside 1–5 | Review rejected |
| 14 | `test_edit_review_success` | Owner edits their own review | 200, review updated in DB |
| 15 | `test_edit_review_requires_login` | Edit a review without being logged in | 302 redirect to login |
| 16 | `test_edit_review_wrong_user_rejected` | User edits someone else's review | Rejected |
| 17 | `test_edit_nonexistent_review` | Edit a review that does not exist | 404 |
| 18 | `test_delete_review_success` | Owner deletes their own review | 200, review removed from DB |
| 19 | `test_delete_review_requires_login` | Delete a review without being logged in | 302 redirect to login |
| 20 | `test_delete_review_wrong_user_rejected` | User deletes someone else's review | Rejected |
| 21 | `test_delete_nonexistent_review` | Delete a review that does not exist | 404 |
| 22 | `test_delete_removes_associated_votes` | Deleting a review also removes its votes | Votes removed from DB |

---

### `test_api_saves.py` — API Endpoints & Saved Units

| # | Test | Description | Expected Output |
|---|------|-------------|-----------------|
| 23 | `test_search_returns_all_units_with_empty_query` | Empty search query returns all units | 200, at least 2 units returned |
| 24 | `test_search_filters_by_keyword` | Search by keyword returns matching unit | 200, returns CITS3403 only |
| 25 | `test_search_filters_by_faculty` | Search by faculty returns matching units | 200, returns Science unit only |
| 26 | `test_search_returns_empty_for_no_match` | Search with no matching results | 200, empty list |
| 27 | `test_save_unit_requires_login` | Save a unit without being logged in | 302 redirect to login |
| 28 | `test_save_unit_saves_successfully` | Logged in user saves a unit | 200, `saved: true` |
| 29 | `test_save_unit_toggles_off` | Saving same unit again unsaves it | 200, `saved: false` |
| 30 | `test_save_unit_missing_unit_id` | Save request with no unit_id | 400 |
| 31 | `test_saved_units_requires_login` | Access saved units page without login | 302 redirect |
| 32 | `test_saved_units_page_loads` | Logged in user accesses saved units page | 200 |
| 33 | `test_saved_units_shows_saved_unit` | Saved unit appears on saved units page | Response contains unit code |
| 34 | `test_vote_requires_login` | Vote on a review without being logged in | 302 redirect to login |
| 35 | `test_vote_upvote_review` | Logged in user upvotes a review | 200, upvotes = 1, downvotes = 0 |
| 36 | `test_vote_downvote_review` | Logged in user downvotes a review | 200, downvotes = 1, upvotes = 0 |
| 37 | `test_vote_toggle_off` | Voting same value again removes the vote | 200, upvotes = 0 |
| 38 | `test_vote_own_review_rejected` | User votes on their own review | 403 |

---

### `selenium/test_user_flow.py` — Authentication Browser Tests

| # | Test | Description | Expected Output |
|---|------|-------------|-----------------|
| 39 | `test_register_login_logout_flow` | New user registers, logs out, and logs back in via browser | Dashboard loads after register and login; redirected to /login after logout |
| 40 | `test_login_with_wrong_password_shows_error` | Login with incorrect password shows error toast | Remains on /login, error toast contains "Invalid email or password" |

---

### `selenium/test_search.py` — Search & Filter Browser Tests

| # | Test | Description | Expected Output |
|---|------|-------------|-----------------|
| 41 | `test_search_filters_units_by_keyword` | Typing a unit code in the search box filters cards via AJAX | Only matching unit card shown |
| 42 | `test_faculty_filter_pill_narrows_results` | Clicking a faculty filter pill filters cards to that faculty | Only Science unit shown; pill marked active |

---

### `selenium/test_reviews.py` — Reviews & Saved Units Browser Tests

| # | Test | Description | Expected Output |
|---|------|-------------|-----------------|
| 43 | `test_logged_in_user_can_submit_review` | Logged in user submits a review via the slider form | Review appears on page, review count updates to 1 |
| 44 | `test_logged_in_user_can_save_unit` | Save unit button toggles via AJAX and persists on reload | Button shows "Saved" after click; state persists after page refresh |
| 45 | `test_user_can_edit_their_own_review` | User edits their own review and updated text appears | Updated comment visible, original comment gone |
| 46 | `test_user_can_upvote_another_users_review` | User upvotes another user's review via AJAX | Upvote count increments to 1, button marked active |

---

## Expected Full Suite Output

```
pytest tests/ --ignore=tests/selenium   →  38 passed, 0 failed
pytest tests/selenium                   →   8 passed, 0 failed
pytest tests                            →  46 passed, 0 failed
```

---

## Notes

- The `DeprecationWarning` about `datetime.utcnow()` in test output comes from SQLAlchemy internals. Safe to ignore.
- The `LegacyAPIWarning` about `Query.get()` comes from Flask-SQLAlchemy. Also safe to ignore.
- Unit tests are fully isolated; each test gets a fresh in-memory database via the `app` fixture.
- Selenium tests are fully isolated; the `_reset_db` fixture wipes and re-seeds the database before every test.
- Selenium tests require Chrome to be installed. ChromeDriver is managed automatically via `webdriver-manager`.