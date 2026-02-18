from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    REDIS_URL = os.getenv("REDIS_URL")
    SECRET_KEY = os.getenv("SECRET_KEY")
    MONTHLY_LIMIT = int(os.getenv("MONTHLY_LIMIT", 5000000))
    RATE_LIMIT = int(os.getenv("RATE_LIMIT", 5))
    DATABASE_URL = os.getenv("DATABASE_URL")

settings = Settings()