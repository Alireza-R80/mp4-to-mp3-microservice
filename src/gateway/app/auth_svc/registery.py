import json

import requests
from config import settings
from fastapi import HTTPException, status
from schemas import User


def register(user: User):
    try:
        user = dict(user)
        response = requests.post(
            f"http://{settings.auth_svc_address}/register", data=json.dumps(user)
        )

        if response.status_code == 201:
            return response.json()

        raise HTTPException(
            status_code=response.status_code, detail=response.json()["detail"]
        )
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )
