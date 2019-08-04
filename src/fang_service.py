#!/usr/bin/python3
"""
This is the web app for fang_service.
It can be used for defang/refang of urls.
See README for setup and usage instructions
"""
from flask import Flask, Response, request, jsonify, make_response
from src.fang import Fang

app = Flask(__name__)


def handle_parameters(url):
    """
    Simple helper to handle splitting the URL if there are parameters

    :param url: String. Http://example.com?a=1&b=2
    :return: (String, String): From above example it would return
             ('http://example.com', 'a=1&b=2')
    """
    if '?' in url:
        url, parameters = url.split('?')
        return (url, parameters)
    else:
        return (url, '')


@app.route('/defang_post/', defaults={'url': None}, methods=['POST'])
@app.route("/defang_get/<path:url>", methods=['GET'])
def defang(url):
    """
    This handles both GET and POST requests.
    If a GET request: this pulls everything in the url after /fang/ and
                      puts it in the variable: url.
    If a POST request: This expects a JSON request in the format
                       {'url: 'http://example.com'}

    :returns: (Json, response code). JSON is in the format
              {'url': 'hxxp://defanged[.]com'}
    """
    result = {}
    if request.method == 'POST':
        req_data = request.get_json()
        if req_data is None or req_data.get('url', None) is None:
            result['error'] = "Proper format is JSON request {'url': 'http://example.com'}"
            return make_response(jsonify(result), 400)

        url, parameters = handle_parameters(req_data['url'])
        result['url'] = Fang.defang(url, parameters)
    else:
        # normal get request
        result['url'] = Fang.defang(url, request.query_string.decode("utf-8"))

    return make_response(jsonify(result), 200)


@app.route('/defang_list/', methods=['POST'])
def defang_list():
    """
    This handles POST requests with a JSON list of URL's to defang.
    Expects a POST request in the format {'urls': [url1, url2, url3]}

    :returns: (json, response_code). JSON is in format:
              {'urls': [url1, url2, url3]}
    """
    req_data = request.get_json()
    if req_data.get('urls', None) is None:
        result = {'error': "Proper format is JSON request {'url': ['url1', 'url2', 'etc']}"}
        return make_response(jsonify(result), 400)

    defanged_urls = []
    for bad_url in req_data['urls']:
        url, parameters = handle_parameters(bad_url)
        defanged_urls.append(Fang.defang(url, parameters))

    result = {'urls': defanged_urls}
    return make_response(jsonify(result), 200)


@app.route('/refang_post/', defaults={'url': None}, methods=['POST'])
@app.route("/refang_get/<path:url>", methods=['GET'])
def refang(url):
    """
    This pulls everything in the URL after /defang/ and puts
    it in the variable: url.
    The parameters are pulled separately.
    :param url: String. The url we're making unsafe
    :returns: (Json, response code). JSON is in the format
              {'url': 'http://refanged.com'}
    """
    result = {}
    if request.method == 'POST':
        req_data = request.get_json()
        if req_data.get('url', None) is None:
            result['error'] = "Proper format is JSON request {'url': 'http://example.com'}"
            return make_response(jsonify(result), 400)

        url, parameters = handle_parameters(req_data['url'])
        result['url'] = Fang.refang(url, parameters)
    else:
        # normal GET request
        result['url'] = Fang.refang(url, request.query_string.decode("utf-8"))

    return make_response(jsonify(result), 200)


@app.route('/refang_list/', methods=['POST'])
def refang_list():
    """
    This handles POST requests with a JSON list of URL's to refang.
    Expects a POST request in the format {'urls': [url1, url2, url3]}

    :returns: (json, response_code). JSON is in format:
              {'urls': [url1, url2, url3]}
    """
    req_data = request.get_json()
    if req_data.get('urls', None) is None:
        result = {'error': "Proper format is JSON request {'url': ['url1', 'url2', 'etc']}"}
        return make_response(jsonify(result), 400)

    refanged_urls = []
    for bad_url in req_data['urls']:
        url, parameters = handle_parameters(bad_url)
        refanged_urls.append(Fang.refang(url, parameters))

    result = {'urls': refanged_urls}
    return make_response(jsonify(result), 200)


if __name__ == "__main__":
    app.run(debug=True)
