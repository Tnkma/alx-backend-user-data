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

    def get_user_from_session_id(self, session_id: str) -> str:
        """ Get the user from the session ID

        Args:
            session_id (str): The session ID

        Returns:
            str: returns the corresponding User or None.
        """
        # if session_id is None, return None
        if session_id is None:
            return None
        try:
            # we try to find the user using the session_id
            user = self._db.find_user_by(session_id=session_id)
            # if we found the user, we return the user
            if user:
                return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """ Destroy a session

        Args:
            user_id (int): The user ID

        Returns:
            None
        """
        if user_id is None:
            return None
        # we update the user's session_id to None
        self._db.update_user(user_id, session_id=None)
        return None

    def get_reset_password_token(self, email: str) -> str:
        """Finds the user by email and updates the reset_token

        Args:
            email (str): the user email

        Returns:
            str: the reset token
        """
        try:
            user = self._db.find_user_by(email=email)
            # if the user exist, we generate a uuid
            if not user:
                raise ValueError
            else:
                reset_token = _generate_uuid()
                # we update the user's reset_token
                self._db.update_user(user.id, reset_token=reset_token)
                return reset_token
        except NoResultFound:
            return None
