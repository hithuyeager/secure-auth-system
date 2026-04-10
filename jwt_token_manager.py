from jose import jwt,JWTError,ExpiredSignatureError
from config import settings
from datetime import datetime,timezone,timedelta
from errors import TokenExpired,InvalidToken
from fastapi.security import HTTPAuthorizationCredentials,HTTPBearer
from fastapi import Depends

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_DAYS = settings.REFRESH_TOKEN_EXPIRE_DAYS

bearer_scheme = HTTPBearer()

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp" : expire})
    access_token = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return access_token

def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp" : expire})
    refresh_token = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return refresh_token
def token_rotation(token: str):
    payload = jwt.decode(token,settings.SECRET_KEY,algorithms=[settings.ALGORITHM])
    user_id = payload.get("sub")
    access_token = create_access_token({"sub" :user_id})
    refresh_token = create_refresh_token({"sub" :user_id})
    return {
        "access_token" : access_token,
        "refresh_token" : refresh_token
    }
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token,settings.SECRET_KEY,algorithms=[ALGORITHM])
    except ExpiredSignatureError:
        raise TokenExpired()
    except JWTError:
        raise InvalidToken() 
    else:
        return payload.get("sub")
