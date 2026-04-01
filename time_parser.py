import re
from datetime import datetime, timedelta
from typing import Optional


def parse_time_input(time_str: str) -> int:
    """Parse a time string into a duration in seconds.

    Supports relative durations (e.g., 5m, 1h30m, 90s) and absolute times
    (e.g., 15:30, "3:30 PM").

    Args:
        time_str: The time string to parse.

    Returns:
        The duration in seconds until the specified time.

    Raises:
        ValueError: If the time string cannot be parsed.
    """
    time_str = time_str.strip()
    # Try parsing as relative duration first
    duration_seconds = _parse_relative_duration(time_str)
    if duration_seconds is not None:
        return duration_seconds
    
    # try parsing as absolute time
    duration_seconds = _parse_absolute_time(time_str)
    if duration_seconds is not None:
        return duration_seconds
    
    # If neither parsing method succeeded, raise an error
    raise ValueError(
        f"Unable to parse time string: '{time_str}'. "
        F"Use relative format (e.g., 5m, 1h30m, 90s) or absolute time format (e.g., 15:30, 3:30 PM)."
    )

def _parse_relative_duration(time_str: str) -> Optional[int]:
    """Parse a relative duration string into seconds.

    Supports formats like '5m', '1h30m', '90s'.

    Args:
        time_str: The relative duration string.

    Returns:
        The duration in seconds, or None if parsing fails.
    """
    pattern = re.compile(r'(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?$')
    match = pattern.fullmatch(time_str)
    if not match:
        return None

    hours, minutes, seconds = match.groups(default='0')
    total_seconds = int(hours) * 3600 + int(minutes) * 60 + int(seconds)
    return total_seconds if total_seconds > 0 else None


def _parse_absolute_time(time_str: str) -> Optional[int]:
    """Parse an absolute time string into a duration in seconds from now.

    Supports formats like '15:30' or '3:30 PM'.

    Args:
        time_str: The absolute time string.

    Returns:
        The duration in seconds until the specified time, or None if parsing fails.
    """
    now = datetime.now()
    for fmt in ("%H:%M", "%I:%M %p"):
        try:
            target_time = datetime.strptime(time_str, fmt).replace(
                year=now.year, month=now.month, day=now.day
            )
            if target_time < now:
                target_time += timedelta(days=1)
            return int((target_time - now).total_seconds())
        except ValueError:
            continue
    return None

