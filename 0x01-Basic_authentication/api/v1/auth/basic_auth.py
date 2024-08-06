#!/usr/bin/env python3
"""Basic Authentication module.
"""

from api.v1.auth.auth import Auth

class BasicAuth(Auth):
    """Basic Authentication class.
    """
    
    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """
        Method to extract the Base64 part from the Authorization header for Basic Authentication.

        Args:
            authorization_header (str): The Authorization header.

        Returns:
            str: The Base64 part of the Authorization header or None if conditions are not met.
        """
        if authorization_header is None:
            return None

        if not isinstance(authorization_header, str):
            return None

        if not authorization_header.startswith('Basic '):
            return None

        return authorization_header[6:]  # Return the value after 'Basic ' (6 characters)
