import hmac
import hashlib
from urllib.parse import urlencode


def generate_signature(payload, api_secret):
    query_string = urlencode(payload)
    return hmac.new(
        api_secret.encode(), query_string.encode(), hashlib.sha256
    ).hexdigest()
