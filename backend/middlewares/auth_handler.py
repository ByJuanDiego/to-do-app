from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, HTTPException

from utils.jwt_handler import decode_jwt


class JWTBearer(HTTPBearer):

    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):

        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)

        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not JWTBearer.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid or Expired token!")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    @staticmethod
    def verify_jwt(jwt_token: str) -> bool:

        is_token_valid: bool = False

        payload: dict = decode_jwt(jwt_token)

        if payload:
            is_token_valid = True

        return is_token_valid
