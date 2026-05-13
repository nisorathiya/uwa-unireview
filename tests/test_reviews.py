# unit tests for review submission, editing, and deletion
from app import db
from app.models import Review, Unit, User, Vote


# ── Helper ─────────────────────────────────────────────────────
def submit_review(client, unit_code='CITS3403', overall=4, workload=3,
                  difficulty=3, usefulness=4, comment='This is a test review comment.'):
    return client.post('/review/submit', data={
        'unit_code'        : unit_code,
        'overall_rating'   : overall,
        'workload_rating'  : workload,
        'difficulty_rating': difficulty,
        'usefulness_rating': usefulness,
        'comment'          : comment,
        'year_taken'       : 2024,
        'semester'         : 'S1'
    }, follow_redirects=True)


# ── Submit review ──────────────────────────────────────────────
def test_submit_review_requires_login(client):
    """Unauthenticated user should be redirected to login."""
    response = client.post('/review/submit', follow_redirects=True)
    assert b'Log in' in response.data


def test_submit_review_success(auth_client, app):
    """Logged in user can submit a review successfully."""
    response = submit_review(auth_client)
    assert response.status_code == 200
    with app.app_context():
        review = Review.query.first()
        assert review is not None
        assert review.overall_rating == 4
        assert review.comment == 'This is a test review comment.'


def test_submit_review_duplicate_rejected(auth_client, app):
    """User cannot submit a second review for the same unit."""
    submit_review(auth_client)
    response = submit_review(auth_client)
    assert b'already reviewed' in response.data
    with app.app_context():
        assert Review.query.count() == 1


def test_submit_review_invalid_unit(auth_client):
    """Submitting a review for a non-existent unit returns 404."""
    response = submit_review(auth_client, unit_code='FAKE9999')
    assert response.status_code == 404


def test_submit_review_comment_too_short(auth_client, app):
    """Comment under 20 characters should be rejected — review not saved."""
    submit_review(auth_client, comment='Too short')
    with app.app_context():
        assert Review.query.count() == 0


def test_submit_review_invalid_rating(auth_client, app):
    """Rating outside 1-5 should be rejected — review not saved."""
    submit_review(auth_client, overall=6)
    with app.app_context():
        assert Review.query.count() == 0


# ── Edit review ────────────────────────────────────────────────
def test_edit_review_success(auth_client, app):
    """Owner can edit their own review."""
    submit_review(auth_client)
    with app.app_context():
        review_id = Review.query.first().id

    auth_client.post(f'/review/edit/{review_id}', data={
        'overall_rating'   : 5,
        'workload_rating'  : 5,
        'difficulty_rating': 5,
        'usefulness_rating': 5,
        'comment'          : 'Updated review comment here.'
    }, follow_redirects=True)

    with app.app_context():
        updated = Review.query.filter_by(id=review_id).first()
        assert updated.overall_rating == 5
        assert updated.comment == 'Updated review comment here.'


def test_edit_review_requires_login(client, auth_client, app):
    """Unauthenticated user cannot edit a review."""
    submit_review(auth_client)
    with app.app_context():
        review_id = Review.query.first().id

    response = client.post(f'/review/edit/{review_id}', data={
        'overall_rating'   : 5,
        'workload_rating'  : 5,
        'difficulty_rating': 5,
        'usefulness_rating': 5,
        'comment'          : 'Hacked review.'
    }, follow_redirects=True)
    # review should NOT be updated
    with app.app_context():
        review = Review.query.filter_by(id=review_id).first()
        assert review.overall_rating != 5


def test_edit_review_wrong_user_rejected(client, auth_client, app):
    """A different user cannot edit someone else's review."""
    submit_review(auth_client)
    with app.app_context():
        review_id = Review.query.first().id

    client.post('/register', data={
        'name'    : 'Other User',
        'email'   : 'other@student.uwa.edu.au',
        'password': 'password123',
        'confirm' : 'password123'
    })
    client.post('/login', data={
        'email'   : 'other@student.uwa.edu.au',
        'password': 'password123'
    })

    response = client.post(f'/review/edit/{review_id}', data={
        'overall_rating'   : 1,
        'workload_rating'  : 1,
        'difficulty_rating': 1,
        'usefulness_rating': 1,
        'comment'          : 'Malicious edit.'
    }, follow_redirects=True)
    assert b'only edit your own' in response.data


def test_edit_nonexistent_review(auth_client):
    """Editing a review that doesn't exist returns 404."""
    response = auth_client.post('/review/edit/9999', data={
        'overall_rating'   : 5,
        'workload_rating'  : 5,
        'difficulty_rating': 5,
        'usefulness_rating': 5,
        'comment'          : 'Updated review comment here.'
    }, follow_redirects=True)
    assert response.status_code == 404


# ── Delete review ──────────────────────────────────────────────
def test_delete_review_success(auth_client, app):
    """Owner can delete their own review."""
    submit_review(auth_client)
    with app.app_context():
        review_id = Review.query.first().id

    auth_client.post(f'/review/delete/{review_id}', follow_redirects=True)

    with app.app_context():
        assert Review.query.filter_by(id=review_id).first() is None


def test_delete_review_requires_login(client, app, test_user):
    """Unauthenticated user cannot delete a review."""
    # create review directly in DB
    with app.app_context():
        user = User.query.filter_by(email='testuser@student.uwa.edu.au').first()
        unit = Unit.query.filter_by(code='CITS3403').first()
        review = Review(
            user_id           = user.id,
            unit_id           = unit.id,
            overall_rating    = 4,
            workload_rating   = 3,
            difficulty_rating = 3,
            usefulness_rating = 4,
            comment           = 'Test review comment here.',
            year_taken        = 2024,
            semester          = 'S1'
        )
        db.session.add(review)
        db.session.commit()
        review_id = review.id

    # unauthenticated client (never logged in)
    response = client.post(
        f'/review/delete/{review_id}',
        follow_redirects=False
    )

    # should redirect to login
    assert response.status_code == 302
    assert 'login' in response.headers['Location']

    # review should still exist
    with app.app_context():
        assert Review.query.filter_by(id=review_id).first() is not None


def test_delete_review_wrong_user_rejected(client, auth_client, app):
    """A different user cannot delete someone else's review."""
    submit_review(auth_client)
    with app.app_context():
        review_id = Review.query.first().id

    client.post('/register', data={
        'name'    : 'Other User',
        'email'   : 'other@student.uwa.edu.au',
        'password': 'password123',
        'confirm' : 'password123'
    })
    client.post('/login', data={
        'email'   : 'other@student.uwa.edu.au',
        'password': 'password123'
    })

    response = client.post(
        f'/review/delete/{review_id}',
        follow_redirects=True
    )
    assert b'only delete your own' in response.data
    with app.app_context():
        assert Review.query.filter_by(id=review_id).first() is not None


def test_delete_nonexistent_review(auth_client):
    """Deleting a review that doesn't exist returns 404."""
    response = auth_client.post('/review/delete/9999', follow_redirects=True)
    assert response.status_code == 404


def test_delete_removes_associated_votes(auth_client, client, app):
    """Deleting a review also deletes its associated votes."""
    submit_review(auth_client)
    with app.app_context():
        review_id = Review.query.first().id

    # add vote directly to DB
    with app.app_context():
        from werkzeug.security import generate_password_hash
        voter = User(
            username='voter',
            email='voter@student.uwa.edu.au',
            password_hash=generate_password_hash('password123')
        )
        db.session.add(voter)
        db.session.commit()
        voter_id = voter.id
        db.session.add(Vote(user_id=voter_id, review_id=review_id, value=1))
        db.session.commit()

    # verify vote exists
    with app.app_context():
        assert Vote.query.filter_by(review_id=review_id).count() == 1

    # delete review as original author using auth_client
    auth_client.post(f'/review/delete/{review_id}', follow_redirects=True)

    # verify both gone
    with app.app_context():
        assert Review.query.filter_by(id=review_id).first() is None
        assert Vote.query.filter_by(review_id=review_id).count() == 0