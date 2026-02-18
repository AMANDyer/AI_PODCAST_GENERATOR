from pydantic import BaseModel

class PodcastRequest(BaseModel):
    topic: str
    emotion: str = "neutral"
    voice_gender: str = "male"  # "male" or "female"