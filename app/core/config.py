from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "VEGA LMS Backend"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    SQLALCHEMY_DATABASE_URI: str

    class Config:
        env_file = ".env"

settings = Settings()
