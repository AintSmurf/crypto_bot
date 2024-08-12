import hmac
import hashlib
from urllib.parse import urlencode
from datetime import datetime, timezone
import typing


def generate_signature(payload: typing.Dict, api_secret: str) -> hmac:
    query_string = urlencode(payload)
    return hmac.new(
        api_secret.encode(), query_string.encode(), hashlib.sha256
    ).hexdigest()


def timestamp_to_date(timestamp: str) -> datetime:
    # Convert Unix timestamp (in milliseconds) to a date string
    return datetime.fromtimestamp(int(timestamp) / 1000, tz=timezone.utc).strftime(
        "%Y-%m-%d"
    )


def date_to_timestamp(date_str: str) -> int:
    # Convert date string (e.g., "2024-03-10") to a Unix timestamp in milliseconds
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    return int(dt.timestamp() * 1000)
