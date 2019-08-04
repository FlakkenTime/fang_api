import pytest
import json
from flask import Flask
from src.fang_service import app


ERROR_STANDARD = "Proper format is JSON request {'url': 'http://example.com'}"
ERROR_LIST = "Proper format is JSON request {'url': ['url1', 'url2', 'etc']}"


@pytest.fixture
def client():
    client = app.test_client()
    return client


def test_defang_get(client):
    response = client.get('defang_get/HTTP://example.com')
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    result = response.json
    assert result.get('url', False) is not False
    assert result['url'] == 'hxxp://example[.]com'


def test_defang_post_no_data(client):
    response = client.post('defang_post/')
    assert response.status_code == 400
    assert response.content_type == 'application/json'
    result = response.json
    assert result.get('error', False) is not False
    assert result['error'] == ERROR_STANDARD


def test_defang_post_no_url(client):
    data = {'tacos': 'http://doesnotmatter.com'}
    response = client.post('defang_post/', data=data)
    assert response.status_code == 400
    assert response.content_type == 'application/json'
    result = response.json
    assert result.get('error', False) is not False
    assert result['error'] == ERROR_STANDARD


def test_defang_post_valid(client):
    data = {'url': 'http://tacos.are.great.com'}
    headers = {'Content-Type': 'application/json'}
    response = client.post('defang_post/', data=json.dumps(data), headers=headers)
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    result = response.json
    assert result.get('url', False) is not False
    expected = "hxxp://tacos[.]are[.]great[.]com"
    assert result['url'] == expected


def test_refang_get(client):
    response = client.get('refang_get/hxxp://example[.]com')
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    result = response.json
    assert result.get('url', False) is not False
    assert result['url'] == 'http://example.com'


def test_refang_post_no_data(client):
    response = client.post('refang_post/')
    assert response.status_code == 400
    assert response.content_type == 'application/json'
    result = response.json
    assert result.get('error', False) is not False
    assert result['error'] == ERROR_STANDARD


def test_refang_post_no_url(client):
    data = {'tacos': 'http://doesnotmatter.com'}
    response = client.post('refang_post/', data=data)
    assert response.status_code == 400
    assert response.content_type == 'application/json'
    result = response.json
    assert result.get('error', False) is not False
    assert result['error'] == ERROR_STANDARD


def test_refang_post_valid(client):
    data = {'url': 'hxxp://tacos[.]are[.]great[.]com'}
    headers = {'Content-Type': 'application/json'}
    response = client.post('refang_post/', data=json.dumps(data), headers=headers)
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    result = response.json
    assert result.get('url', False) is not False
    expected = "http://tacos.are.great.com"
    assert result['url'] == expected


def test_defang_list_no_data(client):
    response = client.post('defang_list/')
    assert response.status_code == 400
    assert response.content_type == 'application/json'
    result = response.json
    assert result.get('error', False) is not False
    assert result['error'] == ERROR_LIST


def test_defang_list_no_urls(client):
    data = {'none': 'stuff'}
    response = client.post('defang_list/')
    assert response.status_code == 400
    assert response.content_type == 'application/json'
    result = response.json
    assert result.get('error', False) is not False
    assert result['error'] == ERROR_LIST


def test_defang_list_single(client):
    data = {'urls': ['http://test.com']}
    headers = {'Content-Type': 'application/json'}
    response = client.post('defang_list/', data=json.dumps(data), headers=headers)
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    result = response.json
    assert result.get('urls', False) is not False
    expected = 'hxxp://test[.]com'
    assert len(result['urls']) == 1
    assert result['urls'][0] == expected


def test_defang_list_multiple(client):
    data = {'urls': ['http://test.com',
                     'http://waka.com?a=1&b=2',
                     'HTTP://ultra.test.net?site=http://hello.com'
                     ]}
    headers = {'Content-Type': 'application/json'}
    response = client.post('defang_list/', data=json.dumps(data), headers=headers)
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    result = response.json
    assert result.get('urls', False) is not False
    assert len(result['urls']) == 3
    assert result['urls'][0] == 'hxxp://test[.]com'
    assert result['urls'][1] == 'hxxp://waka[.]com?a=1&b=2'
    assert result['urls'][2] == 'hxxp://ultra[.]test[.]net?site=hxxp://hello[.]com'


def test_refang_list_no_data(client):
    response = client.post('refang_list/')
    assert response.status_code == 400
    assert response.content_type == 'application/json'
    result = response.json
    assert result.get('error', False) is not False
    assert result['error'] == ERROR_LIST


def test_refang_list_no_urls(client):
    data = {'none': 'stuff'}
    response = client.post('refang_list/')
    assert response.status_code == 400
    assert response.content_type == 'application/json'
    result = response.json
    assert result.get('error', False) is not False
    assert result['error'] == ERROR_LIST


def test_refang_list_single(client):
    data = {'urls': ['hxxp://test[.]com']}
    headers = {'Content-Type': 'application/json'}
    response = client.post('refang_list/', data=json.dumps(data), headers=headers)
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    result = response.json
    assert result.get('urls', False) is not False
    expected = 'http://test.com'
    assert len(result['urls']) == 1
    assert result['urls'][0] == expected


def test_refang_list_multiple(client):
    data = {'urls': ['hxxp://test[.]com',
                     'hxxp://waka[.]com?a=1&b=2',
                     'hxxp://ultra[.]test[.]net?site=hxxp://hello[.]com'
                     ]}
    headers = {'Content-Type': 'application/json'}
    response = client.post('refang_list/', data=json.dumps(data), headers=headers)
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    result = response.json
    assert result.get('urls', False) is not False
    assert len(result['urls']) == 3
    assert result['urls'][0] == 'http://test.com'
    assert result['urls'][1] == 'http://waka.com?a=1&b=2'
    assert result['urls'][2] == 'http://ultra.test.net?site=http://hello.com'
