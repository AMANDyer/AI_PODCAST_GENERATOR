from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import base64
import os
import uuid

from app.database import Base, engine, get_db
from app.routers import auth, podcast, admin
from app.utils.auth import get_current_user
from app.services.llm import generate_podcast_script
from app.services.tts import generate_audio
from app.utils.language import detect_language
from app.utils.rate_limiter import check_rate_limit
from app.models.log import UsageLog

app = FastAPI(title="Podcast TTS Service")

# Create tables on startup
Base.metadata.create_all(bind=engine)

# Mount static folder for UI
app.mount("/static", StaticFiles(directory="static"), name="static")

# Mount saved podcasts folder
app.mount("/podcasts", StaticFiles(directory="podcasts"), name="podcasts")

# Include API routers
app.include_router(auth.router)
app.include_router(podcast.router)
app.include_router(admin.router)

@app.get("/")
def root():
    return {"message": "API is running! Try /docs or /static/index.html for UI"}

@app.websocket("/ws")
async def websocket_podcast(websocket: WebSocket, db: Session = Depends(get_db)):
    await websocket.accept()
    try:
        data = await websocket.receive_json()
        api_key = data.get("api_key")
        topic = data.get("topic")
        emotion = data.get("emotion", "neutral")
        voice_gender = data.get("voice_gender", "male")

        if not api_key or not topic:
            await websocket.send_text("API key ya topic missing!")
            await websocket.close()
            return

        user = get_current_user(api_key, db)
        check_rate_limit(user)

        lang = detect_language(topic)

        await websocket.send_text("Gemini se script generate ho raha hai...")

        script = generate_podcast_script(topic, emotion)

        await websocket.send_text("Script ready! Ab audio ban raha hai...")

        # Voice mapping
        if lang == "hi":
            if voice_gender.lower() == "female":
                voice = "hi-IN-SwaraNeural"
            else:
                voice = "hi-IN-MadhurNeural"
        else:
            if voice_gender.lower() == "female":
                voice = "en-US-AriaNeural"
            else:
                voice = "en-US-GuyNeural"

        audio_bytes, text_length, proc_sec, file_bytes = await generate_audio(
            script, emotion, lang, voice=voice
        )

        # Save to folder
        os.makedirs("podcasts", exist_ok=True)
        filename = f"podcast_{user.username}_{uuid.uuid4().hex[:8]}.mp3"
        file_path = os.path.join("podcasts", filename)

        with open(file_path, "wb") as f:
            f.write(audio_bytes)

        audio_url = f"http://127.0.0.1:8000/podcasts/{filename}"

        # Send base64 for instant play
        b64_audio = base64.b64encode(audio_bytes).decode("utf-8")
        await websocket.send_text(f"audio:data:audio/mp3;base64,{b64_audio}")

        # Send saved URL
        await websocket.send_text(f"saved_url:{audio_url}")

        await websocket.send_text("Done! Audio play karo ↑ | Saved link: " + audio_url)

        # Log usage
        log = UsageLog(
            user_id=user.id,
            text_length=text_length,
            processing_time_sec=proc_sec,
            file_size_bytes=file_bytes,
            emotion=emotion,
            language=lang
        )
        db.add(log)
        db.commit()

        user.monthly_usage += text_length
        db.commit()

    except WebSocketDisconnect:
        print("User disconnected")
    except Exception as e:
        await websocket.send_text(f"Error: {str(e)}")
        print(f"WS error: {e}")