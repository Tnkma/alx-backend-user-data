#!/usr/bin/env python3
""" Basic Auth module"""
from api.v1.auth.auth import Auth
import base64


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
            return base64.b64decode(base64_authorization_header).decode('utf-8')
        except Exception:
            return None
