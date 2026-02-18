# AI Podcast Generator

A self-hosted, multi-user AI-powered podcast generator that turns any topic into a natural-sounding audio episode.  
Uses **Gemini** (free tier) for script generation and **Microsoft Edge TTS** (via edge-tts) for high-quality Hindi/English voice synthesis with emotion support.

### Goal of the Project

To create a **privacy-focused, 100% local-control** tool where users can:
- Input any topic (in Hindi or English)
- Choose emotion (happy, sad, neutral)
- Choose voice gender (male/female)
- Get a complete podcast script + polished audio file instantly
- Track per-user usage (characters processed, monthly limits)
- Run everything locally/offline-capable (no paid APIs except optional Gemini)

Perfect for content creators, educators, students, or anyone in Jaipur/Rajasthan who wants custom podcasts without sending data to third-party services.

### Features

- Multi-user support with API key authentication
- Gemini-powered natural conversational script generation (introduction, body, outro)
- Edge TTS for high-quality Hindi & English voices (male/female)
- Basic emotion control (happy = faster/higher pitch, sad = slower/lower pitch)
- Real-time progress via WebSocket UI
- Saves generated podcasts to folder + returns playable URL
- Usage logging + monthly character limit (configurable)
- Docker support (Redis + API in containers)

### Tech Stack

- Backend: FastAPI (Python)
- Database: SQLite
- Caching/Rate Limiting: Redis
- Script Generation: Google Gemini (free tier)
- TTS: Microsoft Edge TTS (edge-tts library)
- UI: Simple HTML + JavaScript + WebSocket
- Containerization: Docker + docker-compose

### Prerequisites

- Python 3.11+
- Docker Desktop (recommended for Redis)
- Git (optional)

### Installation & Setup

#### Option 1: Local Development (Recommended for Testing)

1. **Clone or extract project** (if not already done)

2. **Create virtual environment**

   ```bash
   python -m venv venv
   .\venv\Scripts\activate   # Windows

3. **Install dependencies**
   pip install -r requirements.txt

4. **Create .env file in root**
5. **Start Redis**
6. **Run the app**
   uvicorn app.main:app --reload
7. **Open UI**
   "http://127.0.0.1:8000/static/index.html"
8. **Or Build & run**
   docker-compose up --build
   