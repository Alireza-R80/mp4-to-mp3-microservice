from pydantic import BaseSettings


class Settings(BaseSettings):
    secret_key: str
    algorithm: str
    mysql_host: str
    mysql_user: str
    mysql_password: str
    mysql_database: str

    class Config:
        env_file = ".env"


settings = Settings()
