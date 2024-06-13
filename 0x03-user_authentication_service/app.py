#!/usr/bin/env python3
""" Creates a simple flask app """
from flask import Flask, jsonify, request, abort, make_response
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def hello() -> str:
    """ A get method that returns a json

    Returns:
        str: A jsonified string
    """
    return jsonify({"message": "Bienvenue"})


#  Define a users function that implements the POST /users route.
@app.route('/users', methods=['POST'], strict_slashes=False)
def users() -> str:
    """ implement the end-point to register a user

    Returns:
        str: parameters from the request
    """
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return make_response(
            jsonify({"message": "email already registered"}), 400
            )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
