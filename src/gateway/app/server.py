import gridfs
import pika
from auth.validate import token as validate_token
from auth_svc import access, registery
from bson.objectid import ObjectId
from database import mp3s_db, videos_db
from fastapi import Depends, FastAPI, HTTPException, UploadFile, status
from fastapi.responses import FileResponse
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


@server.get("/download")
def download(fid: str, access: dict = Depends(validate_token)):
    try:
        out = fs_mp3s.get(ObjectId(fid))

        with open(f"{fid}.mp3", "wb") as f:
            f.write(out.read())

        return FileResponse(f"{fid}.mp3", filename=f"{fid}.mp3")
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="internal server error",
        )
