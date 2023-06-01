import json

import pika
from fastapi import HTTPException, status


def upload(file, fs, channle, access):
    try:
        fid = fs.put(file)

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )

    message = {"video_id": fid, "mp3_id": None, "user_id": access["id"]}

    try:
        channle.basic_publish(
            exchange="",
            routing_key="video",
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ),
        )

    except Exception:
        fs.delete(fid)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )
