import os
from pathlib import Path
from pydantic import BaseModel

BASE_DIR = Path("f:/Work/bragvideoyt").resolve()
OUTPUT_ROOT = BASE_DIR / "THE_HIDDEN_SYSTEMS"
BACKEND_DIR = BASE_DIR / "backend"
DB_PATH = BACKEND_DIR / "studio.db"
TEMPLATES_DIR = BACKEND_DIR / "app" / "templates"
STATIC_DIR = BACKEND_DIR / "static"

OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)
STATIC_DIR.mkdir(parents=True, exist_ok=True)

class Settings(BaseModel):
    app_name: str = "THE HIDDEN SYSTEMS STUDIO"
    channel_name: str = "THE HIDDEN SYSTEMS"
    channel_niche: str = "Artificial Intelligence, Hidden Internet Infrastructure, Digital Mysteries, Science & Future Technology"
    target_video_duration_minutes: int = 12
    words_per_minute: int = 145
    min_script_words: int = 1400
    max_script_words: int = 2200
    critic_min_pass_score: int = 85
    viewer_min_pass_score: int = 85
    default_tts_voice: str = "en-US-ChristopherNeural"
    tts_provider: str = "edge_tts"  # 'edge_tts', 'kokoro', 'elevenlabs'
    video_width: int = 1920
    video_height: int = 1080
    video_fps: int = 30
    daily_schedule_time: str = "06:00"
    daily_schedule_enabled: bool = True
    max_correction_cycles: int = 2
    daily_spend_limit_usd: float = 10.0
    monthly_spend_limit_usd: float = 150.0

settings = Settings()
