#!/usr/bin/env python3
"""Authentication module.
"""


from flask import request
from typing import List, TypeVar

class Auth:
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Method to check if authentication is required.
        Currently, it just returns False.
        
        Args:
            path (str): The path to check.
            excluded_paths (List[str]): A list of paths that do not require authentication.
        
        Returns:
            bool: False for now, as logic will be implemented later.
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        Method to get the authorization header from the request.
        Currently, it returns None.
        
        Args:
            request: The Flask request object.
        
        Returns:
            str: None for now, as logic will be implemented later.
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Method to get the current user from the request.
        Currently, it returns None.
        
        Args:
            request: The Flask request object.
        
        Returns:
            User: None for now, as logic will be implemented later.
        """
        return None
