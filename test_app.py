
from app import create_app
from redis_votes import RedisVotes
from fakeredis import FakeStrictRedis


def test_initial_results():
    votes = RedisVotes(FakeStrictRedis())
    app = create_app(votes)
    app.testing = True
    client = app.test_client()

    response = client.get('/results')
    assert response.status_code == 200
    assert response.json['yes'] == 0
    assert response.json['no'] == 0


def test_can_post_vote():
    votes = RedisVotes(FakeStrictRedis())
    app = create_app(votes)
    app.testing = True
    client = app.test_client()

    response = client.post('/vote', json={'vote': 'yes'})
    assert response.status_code == 200
    assert response.json['yes'] == 1
    assert response.json['no'] == 0


def test_bad_vote_message_body():
    votes = RedisVotes(FakeStrictRedis())
    app = create_app(votes)
    app.testing = True
    client = app.test_client()

    response = client.post('/vote', json={})
    assert response.status_code == 400
    assert response.data == b'Invalid body'


def test_bad_vote_message_vote():
    votes = RedisVotes(FakeStrictRedis())
    app = create_app(votes)
    app.testing = True
    client = app.test_client()

    response = client.post('/vote', json={'vote': 'void'})
    assert response.status_code == 400
    assert response.data == b'Invalid vote'