from sqlalchemy import Column, Integer, String, BigInteger, Boolean
from ..database import Base
from ..config import settings

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    api_key = Column(String, unique=True, index=True)
    monthly_usage = Column(BigInteger, default=0)
    monthly_limit = Column(BigInteger, default=settings.MONTHLY_LIMIT)
    is_admin = Column(Boolean, default=False)