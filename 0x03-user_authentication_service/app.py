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


# Define a login method that implements the POST /sessions route.
# The request is expected to contain form
# data with "email" and a "password" fields.
@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """ implement the end-point to login a user

    Returns:
        str: _description_
    """
    email = request.form.get('email')
    password = request.form.get('password')
    # If the email and password are not correct
    if not AUTH.valid_login(email, password):
        abort(401)
    # if its correct, create a session
    session_id = AUTH.create_session(email)
    # if session creation fails
    if not session_id:
        abort(401)
    response = make_response(jsonify({"email": email, "message": "logged in"}))
    response.set_cookie("session_id", session_id)
    return response


# logout method that implements the DELETE /sessions route.
@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """ implement the end-point to logout a user

    Returns:
        str: the successful logout message
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    AUTH.destroy_session(user.id)
    response = make_response({"message": "logout successful"})
    response.set_cookie("session_id", "", expires=0)
    response.status_code = 302
    return response


# add a GET /profile route that returns a JSON response.
@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> str:
    """ implement the end-point to get the user profile

    Returns:
        str: the user profile
    """
    session_id = request.cookies.get('session_id')
    if not session_id:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    # if the user exist
    if not user:
        abort(403)
    return jsonify({"email": user.email}), 200


# implement the reset_password end-point
@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token() -> str:
    """ implement the end-point to get the reset password token

    Returns:
        str: the reset password token
    """
    email = request.form.get('email')
    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token})
    except ValueError:
        abort(403)


# implement the update_password end-point
@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password() -> str:
    """ implement the end-point to update the password

    Returns:
        str: the updated password
    """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    password_changed = False
    try:
        AUTH.update_password(reset_token, new_password)
        password_changed = True
    except ValueError:
        if not password_changed:
            abort(403)
    return jsonify({"email": email, "message": "Password updated"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
