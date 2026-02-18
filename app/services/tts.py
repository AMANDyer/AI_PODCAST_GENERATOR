import asyncio
from edge_tts import Communicate
import io
import time

async def async_generate_audio(text: str, voice: str = "hi-IN-MadhurNeural", rate: str = "+0%") -> bytes:
    communicate = Communicate(text, voice, rate=rate)
    audio_io = io.BytesIO()

    try:
        async for chunk in communicate.stream():
            # chunk is dict in recent edge-tts versions
            if isinstance(chunk, dict):
                if chunk.get('type') == 'audio':
                    data = chunk.get('data')
                    if isinstance(data, bytes):
                        audio_io.write(data)
            elif isinstance(chunk, bytes):
                # fallback for older versions
                audio_io.write(chunk)
    except Exception as e:
        print(f"TTS stream error: {e}")
        return b''  # return empty on error

    return audio_io.getvalue()


async def generate_audio(script: dict, emotion: str = "neutral", lang: str = "en", voice: str = None) -> tuple[bytes, int, int, int]:
    full_text = f"{script.get('introduction', '')} {script.get('body', '')} {script.get('outro', '')}".strip()
    text_length = len(full_text)
    start_time = time.time()

    # Voice fallback + validation
    if voice is None:
        voice = "hi-IN-MadhurNeural" if lang == "hi" else "en-US-AriaNeural"

    valid_voices = [
        "hi-IN-MadhurNeural", "hi-IN-SwaraNeural",
        "en-US-AriaNeural", "en-US-GuyNeural"
    ]

    if voice not in valid_voices:
        voice = "hi-IN-MadhurNeural" if lang == "hi" else "en-US-AriaNeural"

    rate = "+0%"
    if emotion.lower() == "happy":
        rate = "+15%"
    elif emotion.lower() == "sad":
        rate = "-20%"

    audio_bytes = await async_generate_audio(full_text, voice, rate)

    proc_sec = int(time.time() - start_time)
    file_bytes = len(audio_bytes)

    return audio_bytes, text_length, proc_sec, file_bytes