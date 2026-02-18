import google.generativeai as genai
import json
from app.config import settings
from app.utils.language import detect_language

if not settings.GEMINI_API_KEY:
    raise ValueError("Missing GEMINI_API_KEY in .env")

genai.configure(api_key=settings.GEMINI_API_KEY)

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",  # <-- updated to current stable
    generation_config={
        "temperature": 0.75,
        "top_p": 0.95,
        "response_mime_type": "application/json"
    }
)

def generate_podcast_script(topic: str, emotion: str = "neutral") -> dict:
    lang = detect_language(topic)
    lang_text = "पूरी तरह हिंदी में, बोलचाल की भाषा में" if lang == "hi" else "in natural conversational English"

    emo_map = {
        "happy": "खुश, जोशीले और energetic tone में बोलते हुए",
        "sad": "उदास, भावुक और melancholic tone में बोलते हुए",
        "neutral": "सामान्य friendly conversational tone में"
    }
    emo_prompt = emo_map.get(emotion.lower(), "")

    prompt = f"""Topic: '{topic}'

एक natural podcast script बनाओ {lang_text} {emo_prompt}.
Script को engaging रखो जैसे real host audience से बात कर रहा हो।

Output ONLY valid JSON with these exact keys:
{{
  "introduction": "short intro part",
  "body": "main detailed content part",
  "outro": "closing part"
}}

No extra text, no markdown, just clean JSON."""

    try:
        response = model.generate_content(prompt)
        text = response.text.strip()

        # Clean if Gemini adds code blocks
        if text.startswith("```json"):
            text = text.split("```json")[1].split("```")[0].strip()

        return json.loads(text)
    except Exception as e:
        print(f"Gemini error: {e}")
        return {
            "introduction": "Error generating script",
            "body": f"Gemini API issue: {str(e)}. Check quota/key.",
            "outro": "Sorry!"
        }