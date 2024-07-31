#!/usr/bin/env python3
""" Module of Auth views
"""
import os
from flask import jsonify, abort, request
from typing import List, TypeVar


class Auth:
    """ Auth class """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ returns None - flask request object """
        if path is None:
            return True
        elif excluded_paths is None or excluded_paths == []:
            return True
        elif path in excluded_paths:
            return False
        else:
            for i in excluded_paths:
                if i.startswith(path):
                    return False
                if path.startswith(i):
                    return False
                if i[-1] == "*":
                    if path.startswith(i[:-1]):
                        return False
        return True

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Returns a User instance from information from a request object
        """
        return None

    def authorization_header(self, request=None) -> str:
        """ returns request flask header """
        if request is None:
            return None
        header = request.headers.get('Authorization')
        if header is None:
            return None
        return header
    
    def session_cookie(self, request=None):
        """ returns a cookie value from a request call"""
        if request is None:
            return None
        session_name = os.getenv('SESSION_NAME', '_my_session_id')
        return request.cookies.get(session_name)
