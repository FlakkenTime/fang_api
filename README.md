# fang_api

## Info
This is a Proof of Concept for a URL clean / declean service. One set of endpoint accepts a unencoded URL and defangs it while another set of endpoint will refang it. Simple endpoints for GET and POSTs for basic single URLs and specialized POST only endpoint for handling lists of URLs.

## Install
pip3 install flask

pip3 install gunicorn

pip3 install pytest

pip3 install pytest-cov


## Config
1. There is a basic gunicorn config in `resources/config.py` that can be used for further customization

## Run it locally
Basic HTTP for testing: `gunicorn -c resources/config.py src.fang_service:app`

HTTPS: `gunicorn --certfile=server.crt --keyfile=server.key -c resources/config.py src.fang_service:app`

## Run with Docker
1. docker build -t fang_api:latest .
2. docker run --name fang_api -d -p 8000:8000 fang_api
To find the the IP that is needed you can use:
1. docker ps -a     # find the container id
2. docker inspect the_id    # and find the listed address

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
5. defang list request:
```
curl -X POST "http://localhost:8000/defang_list/" -H "Content-Type: application/json" -d '{"urls": ["HTTP://bad.url.com", "http://example.com?a=1&b=2"]}'
```
6. refang list request:
```
curl -X POST "http://localhost:8000/refang_list/" -H "Content-Type: application/json" -d '{"urls": ["hxxp://bad[.]url[.]com", "hxxp://example[.]com?a=1&b=2"]}'
```
7. GET requests can also be easily tested in your browser.

## Unit testing.
Unit tests can be run from the root of the git directory with the following command: `py.test`. This will execute tests on both the web application endpoints and the library.

For a report of line coverage results use: `pytest --cov-report term-missing --cov=src/`
```
Name                  Stmts   Miss  Cover   Missing
---------------------------------------------------
src/__init__.py           0      0   100%
src/fang.py              11      0   100%
src/fang_service.py      57      1    98%   131
---------------------------------------------------
TOTAL                    68      1    99%
```
Missing the `app.run` line in main haha :)
