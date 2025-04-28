import os
from datetime import datetime, timedelta
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from dotenv import load_dotenv
from jwt import PyJWTError
from sqlalchemy.orm import Session
from app.common.db import get_db
from app.modules.models.user import User


load_dotenv()

ALGORITHM = 'HS256'
TOKEN_EXPIRES = 30
SECRET_KEY = os.getenv('SECRET_KEY')

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(minutes=TOKEN_EXPIRES))
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode,
        os.getenv('SECRET_KEY'),
        algorithm=ALGORITHM
    )


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        token = token.split(" ")[1] if " " in token else token

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if not username:
            raise credentials_exception
    except PyJWTError as e:
        raise credentials_exception from e

    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise credentials_exception
    return user
