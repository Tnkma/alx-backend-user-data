#!/usr/bin/env python3
""" Auth module """
import bcrypt
import uuid
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """Hashes a password

    Args:
        password (str): password to hash

    Returns:
        bytes: hashed password
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Generate a uuid

    Raises:
        ValueError: _description_

    Returns:
        str: The generated uuid
    """
    generate_uuid = str(uuid.uuid4())
    return generate_uuid


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user

        Args:
            email (str): email of the user
            password (str): password of the user

        Returns:
            User: the new user thats registered

        Raises:
            ValueError: if the user already exists
        """
        try:
            # check if the user already exists
            user = self._db.find_user_by(email=email)
            # if the user already exists, raise a ValueError
            if user:
                raise ValueError("User {} already exists".format(email))
        except NoResultFound:
            # if not, hash the password and add the user to the database
            hash_password = _hash_password(password)
            user = self._db.add_user(email, hash_password)
        return user

    def valid_login(self, email: str, password: str) -> bool:
        """validate if a password belonging to a user is valid

        Keyword arguments:
        argument -- email and password
        Return: returns true is valid and false is not
        """
        try:
            # first we query the User model to check for the email
            user = self._db.find_user_by(email=email)
            # we check if the password is valid
            passw_check = bcrypt.checkpw(
                password.encode('utf-8'), user.hashed_password
                )
            # if password is valid
            if passw_check:
                return True
        # if the email is not found
        except NoResultFound:
            pass
        return False

    def create_session(self, email: str) -> str:
        """ Creates a session for a user

        Args:
            email (str): is used to find the user corresponding to the email,
            generates a new uuid and stores it in the database as session_id.

        Returns:
            str: returns the session ID as a string.
        """
        try:
            # we try to find the user using the email
            user = self._db.find_user_by(email=email)
            # if we found the user, we generate a new uuid
            if user:
                session_id = _generate_uuid()
                # we update the user's session_id
                self._db.update_user(user.id, session_id=session_id)
                return session_id
        # if the email is not found
        except NoResultFound:
            pass
        return None
