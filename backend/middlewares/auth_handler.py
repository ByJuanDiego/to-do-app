from fastapi import Request, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordBearer

from jwt import DecodeError

from utils.jwt_handler import verify_jwt, decode_jwt

from typing import Annotated

from config.database import Session, get_db

from schemas.user import UserLogin

from services.user import UserService


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")


class JWTBearer(HTTPBearer):

    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):

        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)

        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid authentication scheme.")
            if not verify_jwt(credentials.credentials):
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid or Expired token!")
            return credentials.credentials
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid authorization code.")


class OAuth2Bearer:

    def __init__(self):
        pass

    def __call__(self, token: Annotated[str, Depends(oauth2_scheme)],
                 db: Annotated[Session, Depends(get_db)]) -> UserLogin:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={
                "WWW-Authenticate": "Bearer"
            },
        )

        try:
            payload: dict = decode_jwt(token)
            username: str = payload.get("username")
            if username is None:
                raise credentials_exception

        except DecodeError:
            raise credentials_exception

        service = UserService(db)
        user = service.get_user_by_username(username)

        if not service.exists_user(user):
            raise credentials_exception

        return user


jwt_bearer = JWTBearer()
oauth2_bearer = OAuth2Bearer()
