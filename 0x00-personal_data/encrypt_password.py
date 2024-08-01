#!/usr/bin/env python3
"""
Using the bcrypt package to hash passwords securely.
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hashes the given password using bcrypt with a salt.

    Args:
        password (str): The password to be hashed.

    Returns:
        bytes: The salted and hashed password.
    """
    # Generate a salt
    salt = bcrypt.gensalt()
    # Hash the password with the generated salt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password
