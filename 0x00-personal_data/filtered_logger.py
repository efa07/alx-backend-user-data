#!/usr/bin/env python3
"""
Module for handling Personal Data
"""

import logging
import re
from typing import List


def filter_datum(fields: List[str],
                 redaction: str, message: str, separator: str) -> str:
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


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        message = super().format(record)
        return filter_datum(self.fields, self.REDACTION,
                            message, self.SEPARATOR)


PII_FIELDS = (
    "name",
    "email",
    "phone",
    "address",
    "ssn"
    "password",
    "ip",
    "last_login",
    "user_agent"
)


def get_logger() -> logging.Logger:
    """
    Creates and configures a logger named 'user_data'.

    Returns:
        logging.Logger: Configured logger.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=PII_FIELDS)
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger
