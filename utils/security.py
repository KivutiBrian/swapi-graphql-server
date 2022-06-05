
import strawberry
from datetime import datetime, timedelta
from typing import Any, Union
from jose import JWTError, jwt

# custom imports
from settings.config import settings

@strawberry.type
class User:
    username: str

@strawberry.type
class LoginSuccess:
    username: User

@strawberry.type
class LoginError:
    message: str

LoginResult = strawberry.union("LoginResult", (LoginSuccess, LoginError))



def create_access_token(
    subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": subject}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def validate_token(token: str) -> LoginResult:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
        username: str = payload.get("sub")
        if username is None:
            return LoginError(message="Could not validate credentials")
        else:
            return LoginSuccess(username=username)

    except JWTError as e:
        return LoginError(message="Invalid Token")