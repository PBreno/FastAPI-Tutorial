from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    database_host: str
    database_port: int
    database_name: str
    database_username: str
    database_password: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        sensitive_case = True
        env_file = ".env"


settings = Settings()