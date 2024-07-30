#!/usr/bin/env python3
""" Basic Auth module"""
from typing import TypeVar
import base64
from api.v1.auth.auth import Auth
from models.user import User


class BasicAuth(Auth):
    """ Basic Auth class"""
    pass

    def extract_base64_authorization_header(
        self, authorization_header: str
    ) -> str:
        """ Extracts the base64 part of the Authorization header"""
        if not authorization_header or type(authorization_header) is not str:
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
        self, base64_authorization_header: str
    ) -> str:
        """ Decodes a base64 string"""
        if not base64_authorization_header or type(
            base64_authorization_header
        ) is not str:
            return None
        try:
            return base64.b64decode(
                base64_authorization_header
            ).decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
        self, decoded_base64_authorization_header: str
    ) -> (str, str):
        """ Extracts user credentials"""
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        email = decoded_base64_authorization_header.split(":")[0]
        password = decoded_base64_authorization_header[len(email) + 1:]
        return (email, password)

    def user_object_from_credentials(
        self, user_email: str, user_pwd: str
    ) -> TypeVar('User'):
        """ Returns a User instance"""
        if not user_email or not isinstance(user_email, str):
            return None
        if not user_pwd or not isinstance(user_pwd, str):
            return None
        try:
            # search for the user in the database
            user_list = User.search({"email": user_email})
            if not user_list or user_list == []:
                return None
            for user in user_list:
                if user.is_valid_password(user_pwd):
                    return user
                return None
            return None
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Overloads Auth and retrieves the User instance for a request"""
        if not request:
            return None
        auth_header = self.authorization_header(request)
        if not auth_header:
            return None
        base64_auth_header = self.extract_base64_authorization_header(
            auth_header
        )
        if not base64_auth_header:
            return None
        decoded_auth_header = self.decode_base64_authorization_header(
            base64_auth_header
        )
        if not decoded_auth_header:
            return None
        user_credentials = self.extract_user_credentials(decoded_auth_header)
        if not user_credentials:
            return None
        user = self.user_object_from_credentials(
            user_credentials[0], user_credentials[1]
        )
        return user
