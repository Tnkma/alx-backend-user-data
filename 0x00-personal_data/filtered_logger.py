#!/usr/bin/env python3
""" filtered logger """
from re import sub


def filter_datum(fields, redaction, message, separator) -> str:
    """filter_datum that returns the log message obfuscated

    Args:
        fields (list): a list of strings representing all fields to obfuscate
        redaction (str): a string representing by what the field will be
        message (str): a string representing the log line
        separator (str): the string separator for the fields
    """
    regex_pattern =  f"({'|'.join(fields)})=.+?({separator}|$)"
    return sub(
        regex_pattern,
        lambda m:
        f"{m.group(1)}={redaction}{separator if m.group(2) == separator else ''}",
        message
        )
