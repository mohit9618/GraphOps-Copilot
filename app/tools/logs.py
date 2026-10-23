
from typing import Any


def search_logs(
    logs: list[str],
    keyword: str | None = None,
    limit: int = 20,
) -> list[str]:
    """Search synthetic logs by keyword."""

    if limit <= 0:
        return []

    if keyword is None:
        return logs[:limit]

    keyword = keyword.lower()

    matches = [
        log for log in logs
        if keyword in log.lower()
    ]

    return matches[:limit]


def get_log_context(
    logs: list[str],
    matched_log: str,
    window: int = 2,
) -> list[str]:
    """Return nearby log entries surrounding a matched entry."""

    if window < 0:
        raise ValueError("window must be non-negative")

    try:
        index = logs.index(matched_log)
    except ValueError:
        return []

    start = max(0, index - window)
    end = min(len(logs), index + window + 1)

    return logs[start:end]
