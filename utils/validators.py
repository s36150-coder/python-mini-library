"""
Validators — input validation using regular expressions.

Regular expressions (regex) let us check whether a string matches a pattern.
For example, a valid email must have: text @ text . text
"""
import re

from utils.exceptions import InvalidEmailError

# Regex pattern for a valid email address.
# \S+ means "one or more non-whitespace characters"
EMAIL_PATTERN = re.compile(r"^\S+@\S+\.\S+$")

# A year must be a 4-digit number between 1000 and 2999
YEAR_PATTERN = re.compile(r"^[12]\d{3}$")


def validate_email(email: str) -> str:
    """
    Check that the email matches the expected format.
    Raises InvalidEmailError if not valid.
    Returns the cleaned email if valid.
    """
    email = email.strip()
    if not EMAIL_PATTERN.match(email):
        raise InvalidEmailError(email)
    return email


def validate_year(year_str: str) -> int:
    """
    Check that the year string is a valid 4-digit year.
    Returns the year as an integer.
    Raises ValueError with a clear message if invalid.
    """
    year_str = year_str.strip()
    if not YEAR_PATTERN.match(year_str):
        raise ValueError(f"'{year_str}' is not a valid year. Please enter a 4-digit year (e.g. 2001).")
    return int(year_str)


def validate_non_empty(value: str, field_name: str) -> str:
    """Ensure a string field is not empty or whitespace-only."""
    value = value.strip()
    if not value:
        raise ValueError(f"{field_name} cannot be empty.")
    return value
