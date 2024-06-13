#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine, tuple_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import NoResultFound, InvalidRequestError
from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a new user to the database

        Args:
            email (str): adds the email
            hashed_password (str): hashes and adds the password

        Returns:
            User: The User model
        """
        try:
            new_user = User(email=email, hashed_password=hashed_password)
            self._session.add(new_user)
            self._session.commit()
        except Exception:
            # if the transc fails, we rollback and return to the first state
            self._session.rollback()
            new_user = None
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """Find a user by a given attribute

        Returns:
            User:The first row found in the users table by the given attribute
        Raises:
            NoResultFound: If no user is found that matches the criteria.
            InvalidRequestError: If invalid arguments are passed to the query.
        """
        keys, values = [], []
        for key, value in kwargs.items():
            if hasattr(User, key):
                keys.append(getattr(User, key))
                values.append(value)
            else:
                raise InvalidRequestError
        user = self._session.query(User).filter(
            tuple_(*keys).in_([tuple(values)])
            ).first()
        if user is None:
            raise NoResultFound
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update a user in the database

        Args:
            user_id (int): The user ID
        returns: None
        """
        # find the user by the id
        user = self.find_user_by(id=user_id)
        # iterate over the kwargs
        for key, value in kwargs.items():
            # if the key is an attribute of the user
            if hasattr(user, key):
                # set the attribute to the value
                # or update the user attribute
                setattr(user, key, value)
            else:
                # if the key is not an attribute of the user
                raise ValueError
        # we commit the changes
        self._session.commit()
