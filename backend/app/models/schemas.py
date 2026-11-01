from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
import datetime

class CompetitorVideo(BaseModel):
    title: str
    channel: str
    views: int
    upload_date: str
    url: Optional[str] = None
    subscribers_est: Optional[int] = None
    view_sub_ratio: Optional[float] = None
    quality_assessment: Optional[str] = None

class TopicCandidate(BaseModel):
    id: str
    title: str
    angle: str
    niche: str
    curiosity_score: float = Field(ge=0, le=100)
    demand_score: float = Field(ge=0, le=100)
    competition_score: float = Field(ge=0, le=100) # lower saturation = higher score
    content_gap: float = Field(ge=0, le=100)
    evergreen_score: float = Field(ge=0, le=100)
    visual_potential: float = Field(ge=0, le=100)
    research_confidence: float = Field(ge=0, le=100)
    production_difficulty: float = Field(ge=0, le=100)
    opportunity_score: float = Field(ge=0, le=100)
    is_measured_youtube_data: bool = True
    competitor_videos: List[CompetitorVideo] = []
    sources: List[str] = []
    selected: bool = False
    is_backup: bool = False

class FactItem(BaseModel):
    id: str
    claim: str
    primary_source: str
    source_url: Optional[str] = None
    verification_status: str = "VERIFIED" # VERIFIED, UNVERIFIED, CONTESTED
    notes: Optional[str] = None

class ResearchDossier(BaseModel):
    topic_title: str
    topic_angle: str
    key_themes: List[str]
    timeline_events: List[Dict[str, str]]
    technical_mechanisms: List[Dict[str, str]]
    verified_facts: List[FactItem]
    citations: List[str]

class CriticEvaluation(BaseModel):
    attempt: int
    hook_score: int = Field(ge=0, le=100)
    clarity_score: int = Field(ge=0, le=100)
    storytelling_score: int = Field(ge=0, le=100)
    retention_score: int = Field(ge=0, le=100)
    accuracy_score: int = Field(ge=0, le=100)
    originality_score: int = Field(ge=0, le=100)
    pacing_score: int = Field(ge=0, le=100)
    ending_score: int = Field(ge=0, le=100)
    overall_score: int = Field(ge=0, le=100)
    feedback_notes: str
    weak_sections: List[str] = []
    passed: bool = False

class ScriptAct(BaseModel):
    act_number: int
    title: str
    narration: str
    word_count: int
    visual_theme: str
    factual_citations: List[str] = []

class ScriptDocument(BaseModel):
    title: str
    total_words: int
    estimated_duration_sec: int
    acts: List[ScriptAct]
    full_text: str
    critic_history: List[CriticEvaluation] = []
    final_critic_score: int = 0
    approved: bool = False

class StoryboardScene(BaseModel):
    scene_id: int
    act_number: int
    narration_chunk: str
    duration_sec: float
    characters: List[str]
    objects: List[str]
    background_type: str
    animation_instructions: str
    camera_movement: str # e.g. "Slow pan right", "Dynamic zoom in on switch", "Parallax tilt"
    transitions: str # e.g. "Sketch reveal wipe", "Crossfade", "Hard cut"
    sound_design: str # e.g. "Low electrical hum, relay click"
    visual_asset_path: Optional[str] = None
    rendered_video_path: Optional[str] = None
    rendered: bool = False

class ViewerReviewReport(BaseModel):
    total_scenes_reviewed: int
    scene_variety_score: int
    visual_consistency_score: int
    narration_sync_score: int
    subtitle_visibility_score: int
    scene_relevance_score: int
    audio_clarity_score: int
    pacing_score: int
    opening_hook_score: int
    ending_quality_score: int
    overall_quality_score: int
    passed_release_gate: bool
    weak_scene_ids: List[int] = []
    inspection_notes: List[str] = []

class ThumbnailConcept(BaseModel):
    id: int
    title: str
    focal_subject: str
    visual_description: str
    contrast_color: str
    file_path: str

class VideoMetadata(BaseModel):
    title_options: List[str]
    final_title: str
    description: str
    chapters: List[Dict[str, str]]
    tags: List[str]
    hashtags: List[str]
    pinned_comment: str
    source_references: List[str]

class ProductionStage(BaseModel):
    index: int
    key: str
    name: str
    status: str = "pending" # pending, running, completed, failed, skipped
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    progress: int = 0
    message: str = ""
    error: Optional[str] = None
    artifacts: Dict[str, Any] = {}

class ProductionProject(BaseModel):
    id: str
    created_at: str
    date_folder: str
    topic_slug: str
    topic_title: str
    status: str = "idle" # idle, running, completed, failed, paused, awaiting_approval, approved
    current_stage_index: int = 0
    progress_pct: int = 0
    stages: List[ProductionStage] = []
    output_dir: str
    final_mp4_path: Optional[str] = None
    preview_mp4_path: Optional[str] = None
    manifest_path: str
    review_score: Optional[int] = None
    approved_by_user: bool = False
    cost_estimate_usd: float = 0.0
    data: Dict[str, Any] = {}

class SystemTelemetry(BaseModel):
    cpu_percent: float
    ram_used_gb: float
    ram_total_gb: float
    ram_percent: float
    disk_free_gb: float
    disk_total_gb: float
    gpu_name: Optional[str] = None
    gpu_vram_used_gb: Optional[float] = None
    gpu_vram_total_gb: Optional[float] = None
    active_workers: int = 0
    scheduler_enabled: bool = True
    next_scheduled_run: str = "06:00:00"
    daily_cost_usd: float = 0.0
    monthly_cost_usd: float = 0.0
    api_status: Dict[str, str] = {}
