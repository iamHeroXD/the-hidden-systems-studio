import os
import subprocess
from pathlib import Path
from typing import Optional, Dict, Any
from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

from backend.app.config import settings, OUTPUT_ROOT, BASE_DIR, TEMPLATES_DIR
from backend.app.database import (
    init_db, get_all_productions, get_production_record,
    save_production_record, get_recent_logs, log_event
)
from backend.app.models.schemas import TopicCandidate
from backend.app.utils.hardware import get_system_telemetry
from backend.app.utils.cost_tracker import CostTracker
from backend.app.agents.topic_engine import TopicIntelligenceEngine
from backend.app.agents.orchestrator import ProductionOrchestrator
from backend.app.automation.scheduler import AutomationScheduler

# Initialize database
init_db()

app = FastAPI(
    title="The Hidden Systems Studio API",
    description="Autonomous AI Animated Documentary Production Platform",
    version="1.0.0"
)

# Enable CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_cleanup_orphans():
    try:
        from backend.app.database import get_connection
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("UPDATE productions SET status = 'interrupted' WHERE status = 'running'")
        conn.commit()
        conn.close()
    except Exception:
        pass

# Static file serving for generated media assets
app.mount("/media", StaticFiles(directory=str(OUTPUT_ROOT)), name="media")

@app.get("/")
def serve_dashboard():
    index_html = TEMPLATES_DIR / "index.html"
    return FileResponse(str(index_html))

@app.get("/api/health")
def health_check():
    prods = get_all_productions()
    telemetry = get_system_telemetry()
    return {
        "status": "healthy",
        "app": "The Hidden Systems Studio",
        "version": "1.2.0-pro",
        "database": "sqlite-wal-ready",
        "productions_count": len(prods),
        "system": telemetry
    }

# --- System & Telemetry Endpoints ---

@app.get("/api/system/status")
def get_status():
    telemetry = get_system_telemetry()
    costs = CostTracker.get_summary()
    sched = AutomationScheduler.get_status()
    return {
        "telemetry": telemetry,
        "costs": costs,
        "scheduler": sched,
        "settings": settings.model_dump()
    }

# --- Topic Intelligence Endpoints ---

@app.get("/api/topics")
def list_topics():
    primary, backups, all_cands = TopicIntelligenceEngine.discover_and_evaluate_topics()
    return {
        "primary": primary.model_dump(),
        "backups": [b.model_dump() for b in backups],
        "candidates": [c.model_dump() for c in all_cands]
    }

class TopicOverrideRequest(BaseModel):
    title: str

@app.post("/api/topics/override")
def override_topic(req: TopicOverrideRequest):
    primary, backups, all_cands = TopicIntelligenceEngine.discover_and_evaluate_topics(manual_override=req.title)
    return {
        "selected": primary.model_dump(),
        "message": f"Primary topic set to: {primary.title}"
    }

# --- Production Studio Endpoints ---

@app.get("/api/progress")
def get_live_progress():
    prods = get_all_productions()
    if not prods:
        return {"status": "idle", "progress_pct": 0, "eta_sec": 0, "elapsed_sec": 0, "stage": "Standby"}
    
    # 1. Target active background thread if currently running
    active_id = getattr(ProductionOrchestrator, "active_production_id", None)
    target = None
    if active_id:
        target = next((p for p in prods if p.get("id") == active_id), None)
        
    # 2. Or most recent production that is marked running
    if not target:
        target = next((p for p in prods if p.get("status") == "running"), None)
        
    # 3. Or most recent production overall
    if not target:
        target = next((p for p in prods if p.get("status") in ["awaiting_approval", "completed"]), prods[0])
        
    live = target.get("live_progress") or {}
    return {
        "id": target.get("id"),
        "title": target.get("topic_title"),
        "status": target.get("status"),
        "progress_pct": target.get("progress_pct", 0),
        "stage_index": target.get("current_stage_index", 0),
        "total_stages": len(target.get("stages", [])),
        "elapsed_sec": target.get("elapsed_sec", 0),
        "eta_sec": target.get("eta_sec", 0),
        "live": live,
        "stages": target.get("stages", [])
    }

@app.get("/api/productions")
def get_productions():
    return get_all_productions()

@app.get("/api/projects")
def get_projects_alias():
    return {"projects": get_all_productions()}

@app.get("/api/productions/{production_id}")
def get_production(production_id: str):
    record = get_production_record(production_id)
    if not record:
        raise HTTPException(status_code=404, detail="Production not found")
    return record

@app.get("/api/projects/{production_id}")
def get_project_alias(production_id: str):
    return get_production(production_id)

class CreateProductionRequest(BaseModel):
    topic_override: Optional[str] = None

@app.post("/api/productions/create")
def create_production(req: CreateProductionRequest):
    project = ProductionOrchestrator.create_project(topic_override=req.topic_override)
    ProductionOrchestrator.start_pipeline_background(project.id)
    return {
        "id": project.id,
        "message": "Production created and pipeline initiated in background thread.",
        "project": project.model_dump()
    }

@app.post("/api/productions/{production_id}/run")
def run_production(production_id: str):
    record = get_production_record(production_id)
    if not record:
        raise HTTPException(status_code=404, detail="Production not found")
    ProductionOrchestrator.start_pipeline_background(production_id)
    return {"message": f"Pipeline started for production {production_id}"}

@app.post("/api/productions/{production_id}/pause")
def pause_production(production_id: str):
    record = get_production_record(production_id)
    if not record:
        raise HTTPException(status_code=404, detail="Production not found")
    record["status"] = "paused"
    save_production_record(record)
    log_event(production_id, "control", "INFO", "Production paused by operator.")
    return {"message": "Production paused."}

@app.post("/api/productions/{production_id}/resume")
def resume_production(production_id: str):
    record = get_production_record(production_id)
    if not record:
        raise HTTPException(status_code=404, detail="Production not found")
    record["status"] = "running"
    save_production_record(record)
    log_event(production_id, "control", "INFO", "Production resumed by operator.")
    ProductionOrchestrator.start_pipeline_background(production_id)
    return {"message": "Production resumed."}

@app.post("/api/productions/{production_id}/approve")
def approve_production(production_id: str):
    record = get_production_record(production_id)
    if not record:
        raise HTTPException(status_code=404, detail="Production not found")
    record["approved_by_user"] = True
    record["status"] = "approved"
    save_production_record(record)
    log_event(production_id, "release", "INFO", "Video approved by human creator for publishing.")
    return {"message": "Video marked approved for YouTube distribution."}

@app.post("/api/productions/{production_id}/open-folder")
def open_folder(production_id: str):
    record = get_production_record(production_id)
    if not record:
        raise HTTPException(status_code=404, detail="Production not found")
    out_dir = record["output_dir"]
    try:
        os.startfile(out_dir)
        return {"message": f"Opened directory: {out_dir}"}
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/productions/{production_id}/export-zip")
def export_project_zip(production_id: str):
    import zipfile
    record = get_production_record(production_id)
    if not record:
        raise HTTPException(status_code=404, detail="Production not found")
    
    out_dir = Path(record["output_dir"])
    zip_path = out_dir / f"{record['topic_slug']}_youtube_package.zip"
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(out_dir):
            for file in files:
                fpath = Path(root) / file
                if fpath.suffix.lower() in [".mp4", ".png", ".srt", ".vtt", ".json", ".txt"]:
                    arcname = fpath.relative_to(out_dir)
                    zipf.write(fpath, arcname)
                    
    return FileResponse(str(zip_path), media_type="application/zip", filename=zip_path.name)

class ProduceTopicRequest(BaseModel):
    title: str

@app.post("/api/topics/produce")
def produce_topic_now(req: ProduceTopicRequest):
    project = ProductionOrchestrator.create_project(topic_override=req.title)
    ProductionOrchestrator.start_pipeline_background(project.id)
    return {
        "message": f"Production initiated for topic: '{req.title}'",
        "project_id": project.id
    }

# --- Logs Endpoints ---

@app.get("/api/logs")
def get_logs(production_id: Optional[str] = None, limit: int = 100):
    return get_recent_logs(production_id=production_id, limit=limit)

# --- Automation Endpoints ---

@app.post("/api/automation/trigger-now")
def trigger_automation_now():
    project = ProductionOrchestrator.create_project()
    ProductionOrchestrator.start_pipeline_background(project.id)
    return {
        "message": f"Automation triggered manually. Production {project.id} started.",
        "production_id": project.id
    }

class ScheduleUpdateRequest(BaseModel):
    enabled: bool
    time_str: str = "06:00"

@app.post("/api/automation/update-schedule")
def update_schedule(req: ScheduleUpdateRequest):
    settings.daily_schedule_enabled = req.enabled
    settings.daily_schedule_time = req.time_str
    if req.enabled:
        AutomationScheduler.register_windows_task(req.time_str)
    else:
        AutomationScheduler.unregister_windows_task()
    return {
        "message": f"Automation schedule updated: enabled={req.enabled}, time={req.time_str}",
        "status": AutomationScheduler.get_status()
    }

# --- Settings Endpoints ---

@app.get("/api/settings")
def get_settings():
    return settings.model_dump()

class SettingsUpdateRequest(BaseModel):
    tts_voice: Optional[str] = None
    daily_spend_limit: Optional[float] = None
    monthly_spend_limit: Optional[float] = None

@app.post("/api/settings/update")
def update_settings(req: SettingsUpdateRequest):
    if req.tts_voice:
        settings.default_tts_voice = req.tts_voice
    if req.daily_spend_limit is not None:
        settings.daily_spend_limit_usd = req.daily_spend_limit
    if req.monthly_spend_limit is not None:
        settings.monthly_spend_limit_usd = req.monthly_spend_limit
    return {"message": "Settings updated successfully.", "settings": settings.model_dump()}
