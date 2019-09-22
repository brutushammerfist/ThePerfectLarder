# Skeleton testing file provided by tutorial located at https://flask.palletsprojects.com/en/1.0.x/testing/

import os
import tempfile

import pytest

from plserver import plserver

@pytest.fixture
def client():
    db_fd, flasker.app.config['DATABASE'] = tempfile.mkstemp()
    plserver.app.config['DATABASE'] = True
    client = plserver.app.test_client()
    
    with plserver.app.app_context():
        plserver.init_db()
        
    yield client
    
    os.close(db_fd)
    on.unlink(plserver.app.config['DATABASE'])
    
def test_empty_db(client):
    rv = client.get('/')
    assert b'No entries here so far' in rv.data
    
def login(client, username, password):
    return client.post('/login', data = dict(username=username, password=password), follow_redirects=True)

def logout(client):
    return client.get('/logout', follow_redirects=True)
    
def test_login_logout(client):
    rv = login(client, plserver.app.config['USERNAME'], plserver.app.config['PASSWORD'])
    assert b'You were logged in' in rv.data
    
    rv = logout(client)
    assert b'You were logged out' in rv.data
    
    rv = login(client, plserver.app.config['USERNAME'] + 'x', plserver.app.config['PASSWORD'])
    assert b'Invalid username' in rv.data
    
    rv = login(client, plserver.app.config['USERNAME'], plserver.app.config['PASSWORD'] + 'x')
    assert b'Invalid password' in rv.data