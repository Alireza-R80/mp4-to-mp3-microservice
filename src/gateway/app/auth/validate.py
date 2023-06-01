import requests
from config import settings
from fastapi import HTTPException, Request, status


def token(request: Request):
    if not "Authorization" in request.headers:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="missing credentials"
        )

    try:
        token = request.headers["Authorization"]
        response = requests.post(
            f"http://{settings.auth_svc_address}/validate",
            headers={"Authorization": token},
        )
        if response.status_code == 200:
            return response.json()

        raise HTTPException(
            status_code=response.status_code, detail=response.json()["detail"]
        )

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )
