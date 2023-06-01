from pydantic import BaseSettings


class Settings(BaseSettings):
    mongodb_host: str
    mongodb_port: str
    auth_svc_address: str

    class Config:
        env_file = ".env"


settings = Settings()
