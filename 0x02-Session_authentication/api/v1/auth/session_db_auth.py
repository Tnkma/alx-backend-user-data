#!/usr/bin/env python3
""" Module for Session DB Authentication """
import uuid
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """SessionDBAuth class to manage session authentication with database"""

    def create_session(self, user_id=None):
        """Create and store a new UserSession instance"""
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Return the User ID by requesting UserSession in the database"""
        if session_id is None or not isinstance(session_id, str):
            return None
        UserSession.load_from_file()  # Ensure we have the latest data
        user_sessions = UserSession.search({'session_id': session_id})
        if not user_sessions:
            return None
        return user_sessions[0].user_id

    def destroy_session(self, request=None):
        """
        Destroy the UserSession based on the
        Session ID from the request cookie
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        UserSession.load_from_file()  # Ensure we have the latest data
        user_sessions = UserSession.search({'session_id': session_id})
        if not user_sessions:
            return False
        user_sessions[0].remove()
        return True
