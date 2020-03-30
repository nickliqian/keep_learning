import responses
import requests
import pytest
from requests.exceptions import ConnectionError


@responses.activate
def test_simple():
    responses.add(responses.GET, 'http://twitter.com/api/1/foobar',
                  json={'error': 'not found'}, status=404)

    resp = requests.get('http://twitter.com/api/1/foobar')

    assert resp.json() == {"error": "not found"}

    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == 'http://twitter.com/api/1/foobar'
    assert responses.calls[0].response.text == '{"error": "not found"}'

    with pytest.raises(ConnectionError):
        requests.get('http://twitter.com/api/1/foobar/2')


@responses.activate
def test_simple2():
    with pytest.raises(ConnectionError):
        requests.get('http://twitter.com/api/1/foobar')


@responses.activate
def test_simple3():
    responses.add(responses.GET, 'http://twitter.com/api/1/foobar',
                  body=IndexError('...'))
    with pytest.raises(IndexError):
        requests.get('http://twitter.com/api/1/foobar')


test_simple3()
