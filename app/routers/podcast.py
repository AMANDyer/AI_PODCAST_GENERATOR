from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
import os
from datetime import datetime
import uuid

from app.database import get_db
from app.utils.auth import get_current_user
from app.services.tts import generate_audio
from app.utils.language import detect_language
from app.services.llm import generate_podcast_script
from app.schemas.podcast import PodcastRequest
from app.models.user import User
from app.models.log import UsageLog

router = APIRouter(prefix="/podcast", tags=["podcast"])

@router.post("/")
def create_podcast(
    request: PodcastRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    lang = detect_language(request.topic)

    # Generate script with Gemini
    script = generate_podcast_script(request.topic, request.emotion)

    # Voice selection
    if lang == "hi":
        if request.voice_gender.lower() == "female":
            voice = "hi-IN-SwaraNeural"
        else:
            voice = "hi-IN-MadhurNeural"
    else:
        voice = "en-US-AriaNeural" if request.voice_gender.lower() == "female" else "en-US-GuyNeural"

    # Generate audio
    audio_bytes, text_length, proc_sec, file_bytes = generate_audio(
        script, request.emotion, lang, voice=voice
    )

    # Save to folder
    os.makedirs("podcasts", exist_ok=True)
    filename = f"podcast_{user.username}_{uuid.uuid4().hex[:8]}.mp3"
    file_path = os.path.join("podcasts", filename)

    with open(file_path, "wb") as f:
        f.write(audio_bytes)

    # Public URL
    audio_url = f"http://127.0.0.1:8000/podcasts/{filename}"

    # Log usage
    log = UsageLog(
        user_id=user.id,
        text_length=text_length,
        processing_time_sec=proc_sec,
        file_size_bytes=file_bytes,
        emotion=request.emotion,
        language=lang
    )
    db.add(log)
    db.commit()

    user.monthly_usage += text_length
    db.commit()

    return {
        "status": "success",
        "audio_url": audio_url,
        "text_length": text_length,
        "processing_sec": proc_sec,
        "message": "Podcast taiyar! Niche link se play/save karo.",
        "filename": filename
    }