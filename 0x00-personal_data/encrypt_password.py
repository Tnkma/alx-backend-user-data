#!/usr/bin/env python3
""" Encrypting passwords """
import bcrypt
from bcrypt import hashpw


def hash_password(password: str) -> bytes:
    """
    Returns a hashed password using bycrpt
    Args:
        password (str): password to be hashed
    """
    b = password.encode()
    hashed = hashpw(b, bcrypt.gensalt())
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Check whether a password is validated
    Args:
        hashed_password (bytes): hashed password
        password (str): password in string
    Return:
        bool
    """
    return bcrypt.checkpw(password.encode(), hashed_password)
