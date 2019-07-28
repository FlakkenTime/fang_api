# fang_api

## Info
This is a Proof of Concept for a URL clean / declean service. One endpoint accepts a unencoded URL and defangs it while another endpoint will refang it.

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
1. defang: `curl "http://localhost:8000/defang/HTTP://bad.url.com"`
2. refang: `curl "http://localhost:8000/refang/hxxp://bad[.]url[.]com"`
3. You can also use the above URLs in your browser.

## Unit testing.
Unit tests can be run from the root of the git directory with the following command: `py.test`
