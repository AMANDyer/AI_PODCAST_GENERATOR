import redis
from fastapi import HTTPException
from datetime import datetime
from app.config import settings
from app.models.user import User

r = redis.from_url(settings.REDIS_URL)

def check_rate_limit(user: User):
    key = f"rate:{user.id}"
    count = r.incr(key)
    if count == 1:
        r.expire(key, 60)  # 1 minute
    if count > settings.RATE_LIMIT:
        raise HTTPException(429, "Rate limit exceeded (wait 1 minute)")

def update_usage(db, user: User, text_len: int, proc_sec: int, file_bytes: int, emotion: str, lang: str):
    month_key = f"usage:{user.id}:{datetime.now().strftime('%Y-%m')}"
    new_total = r.incrby(month_key, text_len)
    if new_total > user.monthly_limit:
        raise HTTPException(402, "Monthly limit exceeded")

    from app.models.log import UsageLog
    log = UsageLog(
        user_id=user.id,
        text_length=text_len,
        processing_time_sec=proc_sec,
        file_size_bytes=file_bytes,
        emotion=emotion,
        language=lang
    )
    db.add(log)
    db.commit()

    user.monthly_usage = new_total
    db.commit()