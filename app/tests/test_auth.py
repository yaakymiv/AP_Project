import secrets
import datetime
from flask import Flask,url_for
from flask_login import current_user, login_user
from app import app, db
import pytest
from app.models import Event, User, UserEvent

def generate_complex_title():
    prefix = 'Event'
    timestamp = datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')
    random_component = secrets.token_hex(4)

    return f'{prefix}_{timestamp}_{random_component}'

@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()

    with app.app_context():
        db.create_all()

    yield client


def test_login_exsists(client):
    response = client.post('/login', data=dict(
        username='john_doe',
        password='pass123'
    ), follow_redirects=True)

    assert response.status_code == 200

def test_login_nonexists(client):
    response = client.post('/login', data=dict(
        username='john_doemsdmd',
        password='pass123dsds'
    ), follow_redirects=True)

    assert response.status_code == 404

def test_logout(client):
    response = client.post('/profile/logout', follow_redirects=True)

    assert response.status_code == 200

def test_register_exists(client):

    response_duplicate = client.post('/register', data=dict(
        username='john_doe',
        email='john@example.com',
        password='pass123'
    ), follow_redirects=True)

    assert response_duplicate.status_code == 409

def test_profile_events_view(client):
    with app.test_request_context('/profile/events'):
        user = User(username='john_doe', email='john@example.com', password='pass123')
        login_user(user)

        response = client.get('/profile/events')
        assert response.status_code == 200


def test_admin_redirect_after_login(client):
    
    response = client.post('/login', data=dict(
        username='admin',
        password='admin123'
    ), follow_redirects=True)

    assert response.status_code == 200 

def test_authenticated_user_redirect_from_login(client):
    with app.test_request_context('/login'):
        user = User(username='john_doe', password='pass123')
        login_user(user)
        response = client.get('/login', follow_redirects=True)
        assert response.status_code == 200  

def test_authenticated_user_redirect_from_register(client):
    with app.test_request_context('/register'):
        user = User(username='john_doe', password='pass123')
        login_user(user)
        response = client.get('/register', follow_redirects=True)
        assert response.status_code == 200  

def test_open_event(client):
    with client:
        client.post('/login', data=dict(
            username='john_doe',
            password='pass123'
        ), follow_redirects=True)

        event_id = 15

        response = client.get(f'/profile/events/{event_id}')

        assert response.status_code == 200

def test_update_event(client):
    with client:
        client.post('/login', data=dict(
            username='john_doe',
            password='pass123'
        ), follow_redirects=True)

        event_id = 15

        response = client.get(f'/profile/events/{event_id}')
        assert response.status_code == 200

        updated_data = {
            'action': 'update',
            'title': 'Updated Event Title',
            'description': 'Updated Event Description',
            'date': '2023-12-31' 
        }

        response = client.post(f'/profile/events/{event_id}', data=updated_data, follow_redirects=True)
        assert response.status_code == 200
        