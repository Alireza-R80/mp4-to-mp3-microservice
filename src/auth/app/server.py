import uvicorn
from database import get_db
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBearer
from models import User
from schemas import UserCreateOut, UserLogin
from sqlalchemy.orm import Session
from utils import create_token, decode_token, get_user

app = FastAPI()
security = HTTPBearer()


@app.post(
    "/register", status_code=status.HTTP_201_CREATED, response_model=UserCreateOut
)
def register(user: UserLogin, db: Session = Depends(get_db)):
    new_user = User(**user.dict())
    user = get_user(user.email, db)

    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exist"
        )

    new_user.create(db)

    return new_user


@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    email = user.email
    password = user.password

    user = get_user(email, db)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    if user.password != password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    token = create_token(user.id, user.email, user.admin)

    return token


@app.post("/validate")
def validate(token: str = Depends(security)):
    decoded_token = decode_token(token.credentials)
    return decoded_token


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
