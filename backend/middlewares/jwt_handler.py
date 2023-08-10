import jwt
import time

import os
from dotenv import load_dotenv


load_dotenv()


JWT_KEY = os.environ["KEY"]
JWT_ALGORITHM = os.environ["ALGORITHM"]


def token_response(token: str) -> dict: 
    return {
        "access-token": token
    }


def sign_jwt(username: str) -> dict:

    payload = {
        "username": username,
        "expiry": time.time() + 600
    }

    token: str = jwt.encode(payload, JWT_KEY, algorithm=JWT_ALGORITHM)
    return token_response(token=token)


def decode_jwt(token: str) -> dict:
    try:
        decode_token: dict = jwt.decode(token, JWT_KEY, algorithms=[JWT_ALGORITHM])
        return decode_token if decode_token['expires'] >= time.time() else None
    except:
        return {}
