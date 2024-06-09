#!/usr/bin/env python3
""" filtered logger """
import re


def filter_datum(fields, redaction, message, separator) -> str:
    """filter_datum that returns the log message obfuscated

    Args:
        fields (list): a list of strings representing all fields to obfuscate
        redaction (str): a string representing by what the field will be
        message (str): a string representing the log line
        separator (str): the string separator for the fields
    """
    pattern = f"({'|'.join(fields)})=([^\\{separator}]*)"
    return re.sub(pattern, lambda m: f"{m.group(1)}={redaction}", message)
