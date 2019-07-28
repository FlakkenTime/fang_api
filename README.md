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
1. simple defang: `curl "http://localhost:8000/defang/HTTP://bad.url.com"`
2. simple refang: `curl "http://localhost:8000/refang/hxxp://bad[.]url[.]com"`

## Unit testing.
upcoming
