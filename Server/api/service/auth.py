from core.auth.auth import authenticate_user, create_access_token
from datetime import timedelta
from config import Config
from core.schemas.token import Token
from core.exceptions.auth_exception import AuthException

from uvicorn.config import logger


async def login_service(form_data) -> Token:
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise AuthException(message="Incorrect username or password")
    access_token_expires = timedelta(minutes=int(Config.ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    logger.info(f"User {form_data.username} logged in")
    return Token(access_token=access_token, token_type="bearer")
