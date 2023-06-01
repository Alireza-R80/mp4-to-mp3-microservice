import json

import requests
from config import settings
from fastapi import HTTPException, status
from schemas import User


def login(user: User):
    try:
        user = dict(user)
        response = requests.post(
            f"http://{settings.auth_svc_address}/login", data=json.dumps(user)
        )

        if response.status_code == 200:
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
