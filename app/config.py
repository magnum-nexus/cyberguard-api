import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    API_KEY = os.getenv("API_KEY", "cyberguard-secret-key-123")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///cyberguard.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False