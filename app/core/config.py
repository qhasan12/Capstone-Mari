import os
from dotenv import load_dotenv

load_dotenv()

class Settings:

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./hrms.db")
    # print(os.getenv("DATABASE_URL"))

    # App
    APP_NAME: str = "HRMS API"

    # JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "super-secret-key")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60)
    )

    # SMTP Email (for OTP)
    SMTP_HOST: str = os.getenv("SMTP_HOST", "")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", 587))
    SMTP_EMAIL: str = os.getenv("SMTP_EMAIL", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")


settings = Settings()