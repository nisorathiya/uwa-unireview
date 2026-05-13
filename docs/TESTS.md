# Testing Documentation

## Overview

UniReview uses **pytest** and **pytest-flask** for unit testing. Tests are isolated using an in-memory SQLite database so they never touch the development or production database.

---

## Technology Stack

| Component | Technology |
|-----------|------------|
| Test framework | pytest |
| Flask integration | pytest-flask |
| Test database | In-memory SQLite (via `TestConfig`) |
| HTML reports | pytest-html |

---

## How to Run

### Install dependencies
```bash
pip install -r requirements.txt
```

### Run all tests
```bash
pytest tests/ -v
```

### Run a single test file
```bash
pytest tests/test_auth.py -v
pytest tests/test_reviews.py -v
pytest tests/test_api_saves.py -v
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
├── conftest.py          # shared fixtures
├── test_auth.py         # authentication route tests
├── test_reviews.py      # review submit/edit/delete tests
└── test_api_saves.py    # API endpoints and saved units tests
```

### Shared Fixtures (`conftest.py`)

All fixtures are available to every test file automatically.

| Fixture | Description |
|---------|-------------|
| `app` | Creates a test Flask app with `TestConfig` — in-memory SQLite, CSRF disabled. Seeds two test units (`CITS3403`, `PSYC1101`). Tears down after each test. |
| `client` | Flask test client for unauthenticated requests. |
| `test_user` | Creates a user (`testuser@student.uwa.edu.au`) in the test DB. |
| `auth_client` | A test client already logged in as `test_user`. |

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

## Expected Full Suite Output

```
38 passed, 0 failed
```

---

## Selenium Tests

*Coming soon — see Issue #61.*

---

## Notes

- The `DeprecationWarning` about `datetime.utcnow()` in test output comes from SQLAlchemy internals — not your code. Safe to ignore.
- The `LegacyAPIWarning` about `Query.get()` comes from Flask-SQLAlchemy — also safe to ignore.
- Tests are fully isolated — each test gets a fresh database via the `app` fixture.