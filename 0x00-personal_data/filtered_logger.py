#!/usr/bin/env python3
"""
Module for handling Personal Data
"""

import bcrypt
import logging
import re
from typing import List
import mysql.connector
import os


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


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Establishes and returns a connection to the MySQL database.

    Returns:
        mysql.connector.connection.MySQLConnection: Database connection object.
    """
    db_config = {
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'host': os.getenv('DB_HOST'),
        'database': os.getenv('DB_NAME')
    }

    connection = mysql.connector.connect(**db_config)
    return connection


def main():
    """
    Main function to retrieve and display users from the database.
    """
    logger = get_logger()
    connection = get_db()

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()

        for row in rows:
            message = "; ".join(f"{key}={value}" for key, value in row.items())
            logger.info(message)
    except mysql.connector.Error as err:
        logger.error(f"Error: {err}")
    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    main()
