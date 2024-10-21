import base64
import json
from datetime import datetime, timedelta
from pprint import pprint
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app import schemas, database, models

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    enconded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return enconded_jwt


def verify_access_token(token: Annotated[str, Depends(oauth2_scheme)], credentials_exception):

    try:
        payload = token.split(".")[1]
        payload += "=" * ((4 - len(payload) % 4) % 4)
        decoded_payload = base64.b64decode(payload).decode("utf-8")
        id: str =json.loads( decoded_payload).get('user_id')
        print("ID ", id)
        if id is None:
            raise credentials_exception

        token_data = schemas.TokenData(id=str(id))
    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(database.get_db)):

    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.user_id).first()

    return user