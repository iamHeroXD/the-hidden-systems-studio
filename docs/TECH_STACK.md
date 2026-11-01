# Technology Stack Specification: The Hidden Systems Studio

## 1. System Topology Overview

```
                                +-----------------------------+
                                |  Next.js 14+ Desktop UI     |
                                |  (TypeScript, Tailwind CSS) |
                                |  Port 3000                  |
                                +--------------+--------------+
                                               |
                                     REST / WebSocket API
                                               |
                                               v
+-----------------------------------------------------------------------------------------+
|                               FastAPI Production Backend (Port 8000)                   |
|                                                                                         |
|  +--------------------+   +-----------------------+   +------------------------------+  |
|  | Multi-Agent Engine |   | Pipeline Orchestrator |   | Hardware & Resource Monitor  |  |
|  | - Topic Discovery  |   | - Checkpoint Manager  |   | - CPU, RAM, Disk, GPU metrics|  |
|  | - Script & Critic  |   | - SQLite Project DB   |   | - Cost tracker & budget guard|  |
|  | - Storyboard / Dir |   | - Background Queue    |   | - Task Scheduler Integration |  |
|  +--------------------+   +-----------------------+   +------------------------------+  |
|                                      |                                                  |
|                                      v                                                  |
|  +-----------------------------------------------------------------------------------+  |
|  |                                Tool & Engine Adapters                             |  |
|  |  +----------------+  +------------------+  +-----------------+  +---------------+ |  |
|  |  | Motion Canvas  |  | Kokoro / Edge    |  | Faster-Whisper  |  | FFmpeg Muxer  | |  |
|  |  | & Rough.js SVG |  | TTS Engine       |  | Subtitle Engine |  | & Normalizer  | |  |
|  |  +----------------+  +------------------+  +-----------------+  +---------------+ |  |
|  |  +----------------+  +------------------+  +-----------------+  +---------------+ |  |
|  |  | yt-dlp & Data  |  | Pillow / OpenCV  |  | ComfyUI / Model |  | Windows Task  | |  |
|  |  | Research Engine|  | Frame Quality QC |  | Diffusion Adap. |  | Scheduler CLI | |  |
|  |  +----------------+  +------------------+  +-----------------+  +---------------+ |  |
|  +-----------------------------------------------------------------------------------+  |
+-----------------------------------------------------------------------------------------+
                                               |
                                               v
                  +----------------------------------------------------------+
                  |  Local File System Storage Structure                     |
                  |  f:\Work\bragvideoyt\THE_HIDDEN_SYSTEMS\YYYY-MM-DD\topic |
                  +----------------------------------------------------------+
```

---

## 2. Component Specifications

### 2.1 Frontend Interface
- **Framework**: Next.js (App Router), React 19, TypeScript
- **Styling**: Tailwind CSS, Lucide React icons, dark minimalist palette (Slate-950 / Zinc-900 / Neutral-900 accents, subtle glowing borders, crisp typography)
- **State Management**: SWR / TanStack Query for live polling & WebSocket for real-time logs and rendering previews
- **Views**:
  1. **Overview Dashboard** (Active production, stage cards, pipeline state, system telemetry, recent videos)
  2. **Topic Intelligence** (Search discoverer, opportunity score matrix, competitor analysis table, topic selector)
  3. **Production Studio** (Live production stepper, scene generation viewer, log stream, manual overrides)
  4. **Script Editor** (Full documentary narrative, act breakdown, research citations, Critic Scorecard)
  5. **Storyboard** (Visual scene timeline, character cues, camera moves, sound design notes)
  6. **Animation Preview** (Interactive Motion Canvas / SVG preview, scene regenerator)
  7. **Voice Studio** (Audio segment waveform playback, TTS voice picker, narration speed control)
  8. **Quality Control** (Automated viewer audit, frame inspection, sync & loudness validation, score > 85/100 gate)
  9. **Video Library** (Historical project gallery, video player, open-in-explorer shortcut)
  10. **Analytics** (Simulated & authorized channel analytics, retention curve estimations)
  11. **Automation** (Windows Task Scheduler controls, daily run-at-06:00 configuration, retry policies)
  12. **Settings** (API keys, provider routing, cost budgets, hardware limits)

### 2.2 Backend Service
- **Framework**: Python 3.14 / FastAPI + Uvicorn
- **Database**: SQLite with WAL (Write-Ahead Logging) mode for concurrent task access without locking
- **ORM / Schemas**: Pydantic v2 + SQLite native / SQLModel
- **Async Runtime**: Python `asyncio` background task pool with persistent task status and step recovery

### 2.3 Agent Architecture
- **State Schema**: Shared JSON-serializable `ProductionProject` model saved at each checkpoint into `manifest.json`
- **Agent Roles**:
  - `DiscoveryAgent`: Queries trends, arXiv, Hacker News, Reddit, YouTube.
  - `CompetitionAgent`: Analyzes video saturation, view count velocity, and audience engagement.
  - `ResearchAgent`: Compiles source facts, timeline of events, and citations.
  - `FactCheckingAgent`: Validates factual claims against primary sources.
  - `StoryDirector`: Outlines 8-stage documentary arc (Hook -> Setup -> Conflict -> Escalation -> Deep Dive -> Revelation -> Climax -> Resolution).
  - `Scriptwriter`: Drafts 1,400–2,000 word conversational, non-robotic narration.
  - `ScriptCritic`: Rigorously evaluates Hook, Clarity, Storytelling, Retention, Accuracy, Originality, Pacing, Ending (Target >= 85/100).
  - `VisualDirector`: Establishes the 2D illustration palette, line weight, and character models.
  - `StoryboardAgent`: Divides script into 35–70 distinct visual scenes.
  - `IllustrationAgent`: Generates SVG / vector assets and character rigs.
  - `AnimationAgent`: Compiles Motion Canvas TSX scene scripts and coordinates rendering.
  - `VoiceAgent`: Synthesizes voice tracks with Kokoro-ONNX / Edge-TTS.
  - `EditorAgent`: Assembles final MP4 with FFmpeg (video, audio, SFX, music, subtitles).
  - `ViewerAgent`: Analyzes rendered frames for visual variety, subtitle readability, and narrative sync.
  - `QualityAgent`: Assesses end-to-end deliverables against release criteria.

### 2.4 Rendering & Video Engine
- **Primary Animation**: Motion Canvas CLI (`@motion-canvas/core`, `@motion-canvas/2d`) + Rough.js
- **Audio Mixing**: FFmpeg with `loudnorm=I=-16:TP=-1.5:LRA=11` (YouTube audio broadcast standard)
- **Subtitles**: Faster-Whisper + FFmpeg `subtitles` filter or standalone SRT/VTT
- **Aspect Ratio**: 1920x1080 (16:9), 30 fps, H.264 video codec, AAC audio codec (192 kbps)

### 2.5 Storage Hierarchy
```
f:\Work\bragvideoyt\THE_HIDDEN_SYSTEMS\
    YYYY-MM-DD\
        [topic-slug]\
            manifest.json
            research\
                sources.json
                fact_check.json
            scripts\
                script_v1.txt
                script_final.txt
                critic_report.json
            storyboard\
                scenes.json
            characters\
                character_sheets.json
                rigs\
            illustrations\
                scene_01.svg
                scene_02.svg
                ...
            animation\
                motion_canvas_project\
                rendered_scenes\
            audio\
                narration_full.wav
                narration_segments\
                bgm.mp3
                sfx\
            subtitles\
                captions.srt
                captions.vtt
            video\
                final_1080p.mp4
                preview_720p.mp4
            thumbnails\
                thumbnail_1.png
                thumbnail_2.png
                thumbnail_3.png
            metadata\
                youtube_metadata.json
            reports\
                viewer_review.json
                quality_gate.json
```
