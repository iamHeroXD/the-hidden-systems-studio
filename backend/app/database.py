import sqlite3
import json
from typing import List, Dict, Any, Optional
from backend.app.config import DB_PATH

def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(str(DB_PATH), timeout=30.0)
    conn.row_factory = sqlite3.Row
    # Enable Write-Ahead Logging (WAL) for concurrency
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA synchronous = NORMAL;")
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Productions Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS productions (
        id TEXT PRIMARY KEY,
        created_at TEXT NOT NULL,
        date_folder TEXT NOT NULL,
        topic_slug TEXT NOT NULL,
        topic_title TEXT NOT NULL,
        status TEXT NOT NULL,
        current_stage_index INTEGER NOT NULL DEFAULT 0,
        progress_pct INTEGER NOT NULL DEFAULT 0,
        output_dir TEXT NOT NULL,
        final_mp4_path TEXT,
        preview_mp4_path TEXT,
        manifest_path TEXT NOT NULL,
        review_score INTEGER,
        approved_by_user INTEGER NOT NULL DEFAULT 0,
        cost_estimate_usd REAL NOT NULL DEFAULT 0.0,
        stages_json TEXT NOT NULL DEFAULT '[]',
        data_json TEXT NOT NULL DEFAULT '{}'
    );
    """)

    # Topics Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS topics (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL UNIQUE,
        angle TEXT NOT NULL,
        niche TEXT NOT NULL,
        curiosity_score REAL NOT NULL,
        demand_score REAL NOT NULL,
        competition_score REAL NOT NULL,
        content_gap REAL NOT NULL,
        evergreen_score REAL NOT NULL,
        visual_potential REAL NOT NULL,
        research_confidence REAL NOT NULL,
        production_difficulty REAL NOT NULL,
        opportunity_score REAL NOT NULL,
        competitor_videos_json TEXT NOT NULL DEFAULT '[]',
        sources_json TEXT NOT NULL DEFAULT '[]',
        selected INTEGER NOT NULL DEFAULT 0,
        is_backup INTEGER NOT NULL DEFAULT 0,
        created_at TEXT NOT NULL
    );
    """)

    # Settings / Key-Value config Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS app_settings (
        key TEXT PRIMARY KEY,
        value TEXT NOT NULL
    );
    """)

    # Production Logs Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS production_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        production_id TEXT NOT NULL,
        stage_key TEXT,
        level TEXT NOT NULL,
        message TEXT NOT NULL,
        timestamp TEXT NOT NULL
    );
    """)

    conn.commit()
    conn.close()

def log_event(production_id: str, stage_key: str, level: str, message: str):
    import datetime
    conn = get_connection()
    try:
        now = datetime.datetime.now().isoformat()
        conn.execute(
            "INSERT INTO production_logs (production_id, stage_key, level, message, timestamp) VALUES (?, ?, ?, ?, ?)",
            (production_id, stage_key, level, message, now)
        )
        conn.commit()
    except Exception as e:
        print(f"Failed to log event: {e}")
    finally:
        conn.close()

def save_production_record(project: Dict[str, Any]):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT OR REPLACE INTO productions (
        id, created_at, date_folder, topic_slug, topic_title, status,
        current_stage_index, progress_pct, output_dir, final_mp4_path,
        preview_mp4_path, manifest_path, review_score, approved_by_user,
        cost_estimate_usd, stages_json, data_json
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, (
        project["id"],
        project["created_at"],
        project["date_folder"],
        project["topic_slug"],
        project["topic_title"],
        project["status"],
        project["current_stage_index"],
        project["progress_pct"],
        project["output_dir"],
        project.get("final_mp4_path"),
        project.get("preview_mp4_path"),
        project["manifest_path"],
        project.get("review_score"),
        1 if project.get("approved_by_user") else 0,
        project.get("cost_estimate_usd", 0.0),
        json.dumps(project.get("stages", [])),
        json.dumps(project.get("data", {}))
    ))
    conn.commit()
    conn.close()

def get_production_record(production_id: str) -> Optional[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productions WHERE id = ?", (production_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return None
    d = dict(row)
    d["stages"] = json.loads(d["stages_json"])
    d["data"] = json.loads(d["data_json"])
    d["approved_by_user"] = bool(d["approved_by_user"])
    return d

def get_all_productions() -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productions ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    results = []
    for row in rows:
        d = dict(row)
        d["stages"] = json.loads(d["stages_json"])
        d["data"] = json.loads(d["data_json"])
        d["approved_by_user"] = bool(d["approved_by_user"])
        results.append(d)
    return results

def get_recent_logs(production_id: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    if production_id:
        cursor.execute("SELECT * FROM production_logs WHERE production_id = ? ORDER BY id DESC LIMIT ?", (production_id, limit))
    else:
        cursor.execute("SELECT * FROM production_logs ORDER BY id DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in reversed(rows)]
