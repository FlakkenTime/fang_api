# fang_api

## Info
This is a Proof of Concept for a URL clean / declean service. One set of endpoint accepts a unencoded URL and defangs it while another set of endpoint will refang it. Supports both GET and POST requests.

## Install
pip3 install flask

pip3 install gunicorn

pip3 install pytest


## Config
1. There is a basic gunicorn config in `resources/config.py` that can be used for further customization

## Run it
Basic HTTP for testing: `gunicorn src.fang_service:app`

HTTPS: `gunicorn --certfile=server.crt --keyfile=server.key src.fang_service:app`

## Direct testing
Note the port can be changed in `resources/config.py`
1. defang GET request: `curl "http://localhost:8000/defang_get/HTTP://bad.url.com"`
2. refang GET request: `curl "http://localhost:8000/refang_get/hxxp://bad[.]url[.]com"`
3. defang POST request:
```
curl -X POST "http://localhost:8000/defang_post/" -H "Content-Type: application/json" -d '{"url": "HTTP://bad.url.com"}'
```
4. refang POST request:
```
curl -X POST "http://localhost:8000/refang_post/" -H "Content-Type: application/json" -d '{"url": "hxxp://bad[.]url[.]com"}'
```
5. You can also use the above URLs in your browser.

## Unit testing.
Unit tests can be run from the root of the git directory with the following command: `py.test`
