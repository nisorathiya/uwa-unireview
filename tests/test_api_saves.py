"""Unit tests for API endpoints and saved units routes."""
import json
from app import db
from app.models import SavedUnit


# ── /api/search ─────────────────────────────────────────────────────────────

def test_search_returns_all_units_with_empty_query(client):
    response = client.get('/api/search')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 2


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
    assert response.status_code == 401 or response.status_code == 302


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