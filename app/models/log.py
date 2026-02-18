from sqlalchemy import Column, Integer, BigInteger, String, DateTime, ForeignKey
from datetime import datetime
from ..database import Base

class UsageLog(Base):
    __tablename__ = "usage_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    text_length = Column(BigInteger)
    processing_time_sec = Column(BigInteger)
    file_size_bytes = Column(BigInteger)
    emotion = Column(String)
    language = Column(String, default="en")
    created_at = Column(DateTime, default=datetime.utcnow)