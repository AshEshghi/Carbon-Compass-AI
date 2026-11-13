"""Input checks shared by the carbon calculation classes."""

from datetime import date, datetime
from math import isfinite


def valid_id(value, name, allow_none=False):
    if allow_none and value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ValueError(f"{name} must be a positive integer" + (" or None" if allow_none else ""))
    return value


def valid_quantity(value, name):
    if isinstance(value, bool):
        raise ValueError(f"{name} must be a finite, non-negative number")
    try:
        number = float(value)
    except (ValueError, TypeError, OverflowError) as exc:
        raise ValueError(f"{name} must be a number") from exc
    if not isfinite(number) or number < 0:
        raise ValueError(f"{name} must be finite and non-negative")
    return number


def valid_timestamp(value):
    if isinstance(value, datetime):
        return value
    if isinstance(value, date):
        return datetime.combine(value, datetime.min.time())
    if isinstance(value, str):
        try:
            return datetime.fromisoformat(value.strip())
        except ValueError as exc:
            raise ValueError("timestamp must be an ISO-formatted date or datetime") from exc
    raise ValueError("timestamp must be a date, datetime, or ISO-formatted string")
