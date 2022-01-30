from datetime import datetime, timedelta
from typing import Optional

from api.dao.user import get_full_user_by_username_dao, get_user_by_username_dao
from config import Config

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from core.schemas.token import TokenData
from core.schemas.user import UserDb

from .hash import verify_password
from ..exceptions.auth_exception import AuthException

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def authenticate_user(username: str, password: str):
    user = get_full_user_by_username_dao(username)

    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=int(Config.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, Config.SECRET_KEY, algorithm=Config.ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserDb:
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=[Config.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise AuthException(message="Invalid token detected")
        token_data = TokenData(username=username)
    except JWTError:
        raise AuthException(message="Invalid token detected")

    user = get_user_by_username_dao(username=token_data.username)
    if user is None:
        raise AuthException(message="Invalid token detected")
    return user

