#!/usr/bin/env python3


import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

    @staticmethod
    def _hash_password(password: str) -> bytes:
        """Hashes a password using bcrypt."""
        import bcrypt
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password

    def register_user(self, email: str, password: str) -> User:
        """Register a new user with hashed password.

        Args:
            email (str): The email of the user.
            password (str): The password of the user.

        Returns:
            User: The newly created User object.

        Raises:
            ValueError: If a user with the given email already exists.
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = self._hash_password(password)
            new_user = self._db.add_user(email=email,
                                         hashed_password=hashed_password)
            return new_user
        except InvalidRequestError as e:
            raise ValueError(f"Invalid request: {e}")

    def valid_login(self, email: str, password: str) -> bool:
        """Check if the provided password matches the hashed password in the
        database.
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                return bcrypt.checkpw(password.encode('utf-8'),
                                      user.hashed_password)
        except Exception:
            return False

        return False
