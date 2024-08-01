#!/usr/bin/env python3
"""
Module for handling Personal Data
"""

import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Redacts specified fields in a log message.

    Args:
        fields (List[str]): List of field names to be redacted.
        redaction (str): The text to replace the field values with.
        message (str): The log message containing fields to be redacted.
        separator (str): The character that separates field values in the
        message.

    Returns:
        str: The message with specified fields redacted.
    """

    return re.sub(rf'({"|".join(fields)})=.+?{separator}',
                  lambda m: f"{m.group(1)}={redaction}{separator}", message)
