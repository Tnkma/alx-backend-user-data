#!/usr/bin/env python3
""" Auth module """
import bcrypt
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
