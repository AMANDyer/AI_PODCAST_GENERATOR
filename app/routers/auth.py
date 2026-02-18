from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserOut
from app.utils.auth import generate_api_key

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserOut)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")
    
    api_key = generate_api_key(user.username)
    db_user = User(username=user.username, api_key=api_key)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return {"username": user.username, "api_key": api_key}