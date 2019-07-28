#!/usr/bin/python3
"""
This is the web app for fang_service.
It can be used for defang/refang of urls.
See README for setup and usage instructions
"""
from flask import Flask, Response, request, jsonify, make_response
from src.fang import Fang

app = Flask(__name__)


@app.route("/defang/<path:url>", methods=['GET'])
def defang(url):
    """
    This pulls everything in the url after /fang/ and
    puts it in the variable: url.
    The parameters are pulled separately.
    :param url: String. The url we're checking for safety
    :returns: (Json, response code). JSON is in the format
              {'url': 'hxxp://defanged[.]com'}
    """
    result = {}
    result['url'] = Fang.defang(url, request.query_string.decode("utf-8"))
    return make_response(jsonify(result), 200)


@app.route("/refang/<path:url>", methods=['GET'])
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
    result['url'] = Fang.refang(url, request.query_string.decode("utf-8"))
    return make_response(jsonify(result), 200)


if __name__ == "__main__":
    app.run(debug=True)
