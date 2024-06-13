#!/usr/bin/env python3
""" Creates a simple flask app """
from flask import Flask, jsonify, request, abort, make_response


app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def hello() -> str:
    """ A get method that returns a json

    Returns:
        str: A jsonified string
    """
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
