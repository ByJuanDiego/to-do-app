import jwt
import time

import os
from dotenv import load_dotenv

import datetime

load_dotenv()

JWT_KEY = os.environ["KEY"]
JWT_ALGORITHM = os.environ["ALGORITHM"]
JWT_EXPIRY_TIME = int(os.environ["EXPIRY_TIME"])


def token_response(token: str) -> dict:
    return {
        "access_token": token,
        "token_type": "bearer"
    }


def sign_jwt(username: str) -> dict:
    payload = {
        "username": username,
        "expires": time.time() + JWT_EXPIRY_TIME
    }

    token: str = jwt.encode(payload, JWT_KEY, algorithm=JWT_ALGORITHM)
    return token_response(token=token)


def decode_jwt(token: str) -> dict:
    try:
        decode_token: dict = jwt.decode(token, JWT_KEY, algorithms=[JWT_ALGORITHM])
        return decode_token if decode_token["expires"] >= time.time() else {}
    except jwt.DecodeError:
        return {}
    except KeyError:
        return {}


def verify_jwt(jwt_token: str) -> bool:
    is_token_valid: bool = False

    payload: dict = decode_jwt(jwt_token)

    if payload:
        is_token_valid = True

    return is_token_valid
