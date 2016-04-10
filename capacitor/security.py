import time
import base64
import hmac
import hashlib
import logging

from capacitor import response


def authenticated(func):
    def wrapper(*args, **kwargs):
        # args[0] is self - current MethodView instance
        self = args[0]
        if not self.current_user:
            return response.forbidden()
        return func(*args, **kwargs)
    return wrapper


def _create_signature(secret, *parts):
    hash = hmac.new(secret, digestmod=hashlib.sha256)
    for part in parts:
        hash.update(part)
    return hash.hexdigest()


def create_signed_value(secret, name, value):
    wall_clock = time.time
    timestamp = str(int(wall_clock()))
    value = base64.b64encode(value)

    signature = _create_signature(secret, name, value, timestamp)
    return '|'.join([value, timestamp, signature])


def _time_independent_equals(a, b):
    return hmac.compare_digest(a, b)


def decode_signed_value(secret, name, value, max_age_days):
    wall_clock = time.time
    parts = value.split('|')
    if len(parts) != 3:
        return None
    signature = _create_signature(secret, name, parts[0], parts[1])
    if not _time_independent_equals(parts[2], signature):
        logging.warning("invalid cookie signature {}".format(value))
        return None
    timestamp = int(parts[1])
    if timestamp < wall_clock() - max_age_days * 86400:
        logging.warning("expired cookie {}".format(value))
    try:
        return base64.b64decode(parts[0])
    except Exception:
        return None

