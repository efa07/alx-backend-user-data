#!/usr/bin/env python3
"""Basic Authentication module.
"""

import base64
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """Basic Authentication class.
    """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        Method to extract the Base64 part from the Authorization header for
        Basic Authentication.

        Args:
            authorization_header (str): The Authorization header.

        Returns:
            str: The Base64 part of the Authorization header or None if
            conditions are not met.
        """
        if authorization_header is None:
            return None

        if not isinstance(authorization_header, str):
            return None

        if not authorization_header.startswith('Basic '):
            return None

        return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        Method to decode a Base64 string.

        Args:
            base64_authorization_header (str): The Base64 encoded string.

        Returns:
            str: The decoded string as a UTF-8 string or None if
            conditions are not met.
        """
        if base64_authorization_header is None:
            return None

        if not isinstance(base64_authorization_header, str):
            return None

        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except Exception:
            return None
