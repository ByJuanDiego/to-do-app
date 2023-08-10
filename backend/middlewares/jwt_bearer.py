from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, HTTPException

from .jwt_handler import decodeJWT, signJWT

from config.database import Session

from models.user import User as UserModel


class JWTBearer(HTTPBearer):
    

    def __init__(self, auto_Error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_Error)


    async def __call__(self, request: Request):

        credentials = HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid or Expired token!")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid or Expired token!")


    def verify_jwt(self, jwtoken: str):

        is_token_valid : bool = False

        payload : dict = decodeJWT(jwtoken)
        
        if payload:
            is_token_valid = True

        return is_token_valid
