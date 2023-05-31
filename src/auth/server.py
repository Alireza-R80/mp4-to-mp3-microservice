import datetime
import os

import jwt
import mysql.connector
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBearer

from .schemas import UserLogin

app = FastAPI()
security = HTTPBearer()

SECRET = os.environ.get("SECRET")
ALGORITHM = "HS256"
connection = mysql.connector.connect(
    host=os.environ.get("MYSQL_HOST"),
    port=os.environ.get("MYSQL_PORT"),
    user=os.environ.get("MYSQL_USER"),
    password=os.environ.get("MYSQL_PASSWORD"),
    database=os.environ.get("MYSQL_DATABASE"),
)


@app.post("/login")
def login(user: UserLogin):
    email = user.email
    password = user.password

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM USER WHERE email=%s", (email,))
    user = cursor.fetchone()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    if user[2] != password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    token = create_token(user[0])

    return token


@app.post("/validate")
def validate(token: str = Depends(security)):
    decoded_token = decode_token(token)
    return decoded_token


def create_token(id):
    payload = {
        "id": id,
        "exp": datetime.datetime.now() + datetime.timedelta(days=1),
        "iat": datetime.datetime.now(),
    }
    token = jwt.encode(payload, SECRET, ALGORITHM)

    return token


def decode_token(token):
    try:
        payload = jwt.decode(token, SECRET, ALGORITHM)
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
