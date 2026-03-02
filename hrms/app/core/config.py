import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./hrms.db")
    APP_NAME: str = "HRMS API"
# print("ENV DB:", os.getenv("DATABASE_URL"))
settings = Settings()