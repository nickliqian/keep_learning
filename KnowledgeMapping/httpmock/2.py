import json

import responses
import requests

@responses.activate
def test_calc_api():

    def request_callback(request):
        payload = json.loads(request.body)
        resp_body = {'value': sum(payload['numbers'])}
        headers = {'request-id': '728d329e-0e86-11e4-a748-0c84dc037c13'}
        return (200, headers, json.dumps(resp_body))

    responses.add_callback(
        responses.POST, 'http://calc.com/sum',
        callback=request_callback,
        content_type='application/json',
    )

    resp = requests.post(
        'http://calc.com/sum',
        json.dumps({'numbers': [1, 2, 3]}),
        headers={'content-type': 'application/json'},
    )

    assert resp.json() == {'value': 6}

    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == 'http://calc.com/sum'
    assert responses.calls[0].response.text == '{"value": 6}'
    assert (
        responses.calls[0].response.headers['request-id'] ==
        '728d329e-0e86-11e4-a748-0c84dc037c13'
    )