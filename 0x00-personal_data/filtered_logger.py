#!/usr/bin/env python3
""" filtered logger """
import re
import logging
from typing import List


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(
        fields: List[str], redaction: str, message: str, separator: str
        ) -> str:
    """filter_datum that returns the log message obfuscated

    Args:
        fields (list): a list of strings representing all fields to obfuscate
        redaction (str): a string representing by what the field will be
        message (str): a string representing the log line
        separator (str): the string separator for the fields
    """
    pattern = f"({'|'.join(fields)})=([^\\{separator}]*)"
    return re.sub(pattern, lambda m: f"{m.group(1)}={redaction}", message)


def get_logger() -> logging.Logger:
    """creates a new logger for the user data

    Returns:
        logging.Logger: a logger object
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    handler = logging.StreamHandler()

    formatter = RedactingFormatter(PII_FIELDS)

    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


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
        """format method that returns the logRecord

        Args:
            record (logging.LogRecord): the incoming log record

        Returns:
            str: returns the filtered value
        """
        incoming_message = super(RedactingFormatter, self).format(record)
        text = filter_datum(
            self.fields, self.REDACTION, incoming_message, self.SEPARATOR
        )
        return text
