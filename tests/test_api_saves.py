"""Unit tests for API endpoints and saved units routes."""
import json
from app import db
from app.models import SavedUnit


# ── /api/search ─────────────────────────────────────────────────────────────

def test_search_returns_all_units_with_empty_query(client):
    response = client.get('/api/search')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) >= 2


def test_search_filters_by_keyword(client):
    response = client.get('/api/search?q=Agile')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 1
    assert data[0]['code'] == 'CITS3403'


def test_search_filters_by_faculty(client):
    response = client.get('/api/search?faculty=Science')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 1
    assert data[0]['code'] == 'PSYC1101'


def test_search_returns_empty_for_no_match(client):
    response = client.get('/api/search?q=nonexistent')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 0


# ── /api/save-unit ───────────────────────────────────────────────────────────

def test_save_unit_requires_login(client, app):
    with app.app_context():
        from app.models import Unit
        unit = Unit.query.filter_by(code='CITS3403').first()
        unit_id = unit.id
    response = client.post('/api/save-unit',
                           data=json.dumps({'unit_id': unit_id}),
                           content_type='application/json')
    assert response.status_code == 302


def test_save_unit_saves_successfully(auth_client, app):
    with app.app_context():
        from app.models import Unit
        unit = Unit.query.filter_by(code='CITS3403').first()
        unit_id = unit.id
    response = auth_client.post('/api/save-unit',
                                data=json.dumps({'unit_id': unit_id}),
                                content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['saved'] is True


def test_save_unit_toggles_off(auth_client, app):
    with app.app_context():
        from app.models import Unit
        unit = Unit.query.filter_by(code='CITS3403').first()
        unit_id = unit.id
    # Save it first
    auth_client.post('/api/save-unit',
                     data=json.dumps({'unit_id': unit_id}),
                     content_type='application/json')
    # Save again to toggle off
    response = auth_client.post('/api/save-unit',
                                data=json.dumps({'unit_id': unit_id}),
                                content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['saved'] is False


def test_save_unit_missing_unit_id(auth_client):
    response = auth_client.post('/api/save-unit',
                                data=json.dumps({}),
                                content_type='application/json')
    assert response.status_code == 400


# ── /saved-units ───────────────────────────────────────────────────────────── 

def test_saved_units_requires_login(client):
    response = client.get('/saved-units', follow_redirects=False)
    assert response.status_code == 302


def test_saved_units_page_loads(auth_client):
    response = auth_client.get('/saved-units')
    assert response.status_code == 200


def test_saved_units_shows_saved_unit(auth_client, app):
    with app.app_context():
        from app.models import Unit
        unit = Unit.query.filter_by(code='CITS3403').first()
        unit_id = unit.id
    auth_client.post('/api/save-unit',
                     data=json.dumps({'unit_id': unit_id}),
                     content_type='application/json')
    response = auth_client.get('/saved-units')
    assert b'CITS3403' in response.data

# ── /api/vote ────────────────────────────────────────────────────────────────

def test_vote_requires_login(client, app):
    with app.app_context():
        from app.models import Unit, Review, User
        from werkzeug.security import generate_password_hash
        user = User(username='reviewer', email='reviewer@student.uwa.edu.au',
                    password_hash=generate_password_hash('password123'))
        unit = Unit.query.filter_by(code='CITS3403').first()
        db.session.add(user)
        db.session.flush()
        review = Review(user_id=user.id, unit_id=unit.id,
                        overall_rating=4, workload_rating=3,
                        difficulty_rating=3, usefulness_rating=4,
                        comment='Good unit overall enjoyed it a lot',
                        year_taken=2024, semester='S1')
        db.session.add(review)
        db.session.commit()
        review_id = review.id
    response = client.post('/api/vote',
                           data=json.dumps({'review_id': review_id, 'value': 1}),
                           content_type='application/json')
    assert response.status_code == 401 or response.status_code == 302


def test_vote_upvote_review(auth_client, app):
    with app.app_context():
        from app.models import Unit, Review, User
        from werkzeug.security import generate_password_hash
        user = User(username='reviewer2', email='reviewer2@student.uwa.edu.au',
                    password_hash=generate_password_hash('password123'))
        unit = Unit.query.filter_by(code='CITS3403').first()
        db.session.add(user)
        db.session.flush()
        review = Review(user_id=user.id, unit_id=unit.id,
                        overall_rating=4, workload_rating=3,
                        difficulty_rating=3, usefulness_rating=4,
                        comment='Good unit overall enjoyed it a lot',
                        year_taken=2024, semester='S1')
        db.session.add(review)
        db.session.commit()
        review_id = review.id
    response = auth_client.post('/api/vote',
                                data=json.dumps({'review_id': review_id, 'value': 1}),
                                content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['upvotes'] == 1
    assert data['downvotes'] == 0


def test_vote_downvote_review(auth_client, app):
    with app.app_context():
        from app.models import Unit, Review, User
        from werkzeug.security import generate_password_hash
        user = User(username='reviewer3', email='reviewer3@student.uwa.edu.au',
                    password_hash=generate_password_hash('password123'))
        unit = Unit.query.filter_by(code='CITS3403').first()
        db.session.add(user)
        db.session.flush()
        review = Review(user_id=user.id, unit_id=unit.id,
                        overall_rating=4, workload_rating=3,
                        difficulty_rating=3, usefulness_rating=4,
                        comment='Good unit overall enjoyed it a lot',
                        year_taken=2024, semester='S1')
        db.session.add(review)
        db.session.commit()
        review_id = review.id
    response = auth_client.post('/api/vote',
                                data=json.dumps({'review_id': review_id, 'value': -1}),
                                content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['downvotes'] == 1
    assert data['upvotes'] == 0


def test_vote_toggle_off(auth_client, app):
    with app.app_context():
        from app.models import Unit, Review, User
        from werkzeug.security import generate_password_hash
        user = User(username='reviewer4', email='reviewer4@student.uwa.edu.au',
                    password_hash=generate_password_hash('password123'))
        unit = Unit.query.filter_by(code='CITS3403').first()
        db.session.add(user)
        db.session.flush()
        review = Review(user_id=user.id, unit_id=unit.id,
                        overall_rating=4, workload_rating=3,
                        difficulty_rating=3, usefulness_rating=4,
                        comment='Good unit overall enjoyed it a lot',
                        year_taken=2024, semester='S1')
        db.session.add(review)
        db.session.commit()
        review_id = review.id
    # Upvote first
    auth_client.post('/api/vote',
                     data=json.dumps({'review_id': review_id, 'value': 1}),
                     content_type='application/json')
    # Toggle off
    response = auth_client.post('/api/vote',
                                data=json.dumps({'review_id': review_id, 'value': 0}),
                                content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['upvotes'] == 0


def test_vote_own_review_rejected(auth_client, app, test_user):
    with app.app_context():
        from app.models import Unit, Review, User
        unit = Unit.query.filter_by(code='CITS3403').first()
        user = User.query.filter_by(username='testuser').first()
        review = Review(user_id=user.id, unit_id=unit.id,
                        overall_rating=4, workload_rating=3,
                        difficulty_rating=3, usefulness_rating=4,
                        comment='Good unit overall enjoyed it a lot',
                        year_taken=2024, semester='S1')
        db.session.add(review)
        db.session.commit()
        review_id = review.id
    response = auth_client.post('/api/vote',
                                data=json.dumps({'review_id': review_id, 'value': 1}),
                                content_type='application/json')
    assert response.status_code == 403