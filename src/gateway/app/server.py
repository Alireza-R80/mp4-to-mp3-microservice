import gridfs
import pika
from auth.validate import token as validate_token
from auth_svc import access, registery
from database import mp3s_db, videos_db
from fastapi import Depends, FastAPI, UploadFile, status
from schemas import User
from storage import utils

server = FastAPI()

fs_videos = gridfs.GridFS(videos_db)
fs_mp3s = gridfs.GridFS(mp3s_db)

connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq-service"))
channle = connection.channel()


@server.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: User):
    response = registery.register(user)
    return response


@server.post("/login")
def login(user: User):
    token = access.login(user)
    return token


@server.post("/upload")
def upload(file: UploadFile, access: dict = Depends(validate_token)):
    utils.upload(file.file, fs_videos, channle, access)

    return "success"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(server, host="0.0.0.0", port=9000)
