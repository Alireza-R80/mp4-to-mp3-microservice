import datetime

import jwt
from config import settings
from fastapi import HTTPException, status
from models import User
from sqlalchemy.orm import Session


def create_token(id, admin):
    payload = {
        "id": id,
        "exp": datetime.datetime.now() + datetime.timedelta(days=1),
        "iat": datetime.datetime.now(),
        "admin": admin,
    }
    token = jwt.encode(payload, settings.secret_key, settings.algorithm)

    return token


def decode_token(token):
    try:
        payload = jwt.decode(token, settings.secret_key, settings.algorithm)
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_user(email, db: Session):
    return db.query(User).filter(User.email == email).first()
