from langdetect import detect, LangDetectException

def detect_language(text: str) -> str:
    """
    Detects if text is Hindi or English (for TTS selection).
    Returns 'hi' for Hindi/Indic, 'en' otherwise.
    """
    try:
        lang = detect(text)
        # Treat many Indian languages as 'hi' for TTS voice
        if lang in ['hi', 'bn', 'mr', 'ta', 'te', 'gu', 'kn', 'ml', 'pa']:
            return "hi"
        return "en"
    except LangDetectException:
        return "en"  # default to English