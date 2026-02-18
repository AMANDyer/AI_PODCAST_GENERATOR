from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.config import settings
import secrets
import base64

def generate_api_key(username: str) -> str:
    # Simple but secure enough for dev – use Fernet later if needed
    raw = f"{username}:{secrets.token_hex(16)}"
    return base64.urlsafe_b64encode(raw.encode()).decode().rstrip("=")

def get_current_user(api_key: str, db: Session = Depends(get_db)) -> User:
    # Very basic check for now – improve later
    try:
        decoded = base64.urlsafe_b64decode(api_key + "==").decode()
        username = decoded.split(":")[0]
        user = db.query(User).filter(User.username == username).first()
        if not user:
            raise HTTPException(401, "Invalid API key")
        return user
    except:
        raise HTTPException(401, "Invalid API key")