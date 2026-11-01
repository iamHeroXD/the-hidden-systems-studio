# THE HIDDEN SYSTEMS STUDIO
### Autonomous AI Animated Documentary Production Platform

**Channel Identity**: THE HIDDEN SYSTEMS  
**Channel Focus**: Artificial Intelligence, Computer Science, Hidden Internet Infrastructure, Digital Mysteries, Future Technology & What-If Scenarios  
**Format**: 10–15 Minute Original Hand-Drawn 2D Animated Explainers  
**Aesthetic**: Editorial hand-drawn organic linework, 1080p 30fps vector animation, broadcast audio (-16 LUFS)  

---

## 1. Quick Start & Execution

### One-Click Launch
Double-click `start_studio.bat` or run in PowerShell:
```powershell
.\start_studio.ps1
```
This automatically initiates:
- **Studio Production Engine & REST API**: [http://localhost:8000](http://localhost:8000)
- **Interactive Production Dashboard**: [http://localhost:8000](http://localhost:8000) (and Next.js on `:3000`)
- **API Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 2. Platform Architecture

The Studio is engineered as an autonomous multi-agent production pipeline orchestrated with persistent SQLite checkpoints and deterministic hardware rendering:

```
[TOPIC INTELLIGENCE] -> [RESEARCH DOSSIER] -> [SCRIPTWRITER & CRITIC]
                                                     |
                                                     v
[AUDIO & SUBTITLES]  <- [STORYBOARD & ASSETS] <- [VISUAL DIRECTOR]
        |
        v
[FFMPEG MUXER]       -> [VIEWER REVIEW AUDIT]  -> [YOUTUBE REPOSITORY FOLDER]
```

### Specialized Autonomous Agents:
1. **Discovery Agent**: Mines 20+ topic opportunities per cycle across research publications, trends, and infrastructure mysteries.
2. **Competition Agent**: Scrapes YouTube competitor metrics (view velocity, saturation, upload dates, view-to-sub ratios).
3. **Research Agent & Fact-Checker**: Compiles source dossiers, timestamps, and verifiable RFC/whitepaper evidence ledgers.
4. **Story Director & Scriptwriter**: Crafts 1,400–2,000 word conversational educational scripts across an 8-act narrative arc.
5. **Script Critic Agent**: Independently scores Hook, Clarity, Storytelling, Retention, Accuracy, Originality, Pacing, and Ending (Pass threshold: >= 85/100).
6. **Visual Director**: Defines the organic editorial linework, character rig ("The Investigator"), and dark neutral color palette.
7. **Storyboard Agent**: Deconstructs narrative into 40 structured scenes with camera directions, transitions, and audio cues.
8. **Illustration Agent**: Procedurally renders 40 high-definition hand-drawn SVGs and companion 1080p graphics.
9. **Animation Agent**: Compiles Motion Canvas project files and executes cinematic FFmpeg camera moves (pans, dynamic zooms, parallax float).
10. **Voice Agent**: Synthesizes broadcast narration via Edge-TTS / Kokoro ONNX neural speech with individual act tracks and master concatenation.
11. **Subtitles Agent**: Produces word-synchronized SRT and VTT captions.
12. **Editor Agent**: Muxes video scenes + narration + procedural ambient soundtrack + sound design with EBU R128 loudness normalization.
13. **Viewer Agent**: Inspects representative extracted frames to verify color contrast, scene variety, and absence of corrupted/black frames.
14. **Quality Agent**: Enforces the >= 85/100 release gate before clearing videos for creator approval.
15. **Packaging Agent**: Generates 3 high-contrast 1280x720 thumbnail designs and comprehensive YouTube metadata (titles, description, chapters, tags).

---

## 3. Daily Automation (Independent of IDE)

The application includes native integration with **Windows Task Scheduler**:
- **Trigger**: Runs every morning at **06:00 AM** local time.
- **Standalone Runner**: `backend/daily_runner.py` executes without needing any IDE or terminal window open.
- **Persistent Checkpoints**: If interrupted or restarted, resuming resumes from the exact failed stage without redoing completed work.
- **Control**: Toggle schedule or trigger manual runs directly from the Automation tab in the dashboard.

---

## 4. First Complete Pilot Deliverable

**Title**: *What If The Entire Internet Disappeared For 24 Hours?*  
**Location**: `THE_HIDDEN_SYSTEMS/2026-11-01/what-if-the-entire-internet-disappeared-/`

```
what-if-the-entire-internet-disappeared-/
├── manifest.json                  # Complete machine-readable production audit
├── video/
│   ├── final_1080p.mp4            # Master 1080p 30fps documentary (148.9 MB)
│   ├── preview_720p.mp4           # Lightweight web preview (53.4 MB)
│   ├── raw_video_stitched.mp4     # Lossless visual scene assembly (139.9 MB)
│   └── ambient_score.mp3          # Procedural ambient documentary soundtrack
├── audio/
│   ├── narration_full.mp3         # Master voice narration (3.75 MB)
│   └── narration_segments/        # 8 Act-by-act audio tracks
├── illustrations/                 # 40 High-definition hand-drawn SVGs & PNGs
├── animation/
│   ├── rendered_scenes/           # 40 Animated 1080p scene clips with camera moves
│   └── motion_canvas_project/     # Motion Canvas TypeScript scene definitions
├── scripts/
│   └── script_final.txt           # 8 Acts (1,820 words conversational English)
├── storyboard/
│   └── scenes.json                # 40 Scenes with camera directions & sound cues
├── subtitles/
│   ├── captions.srt               # SRT subtitles with millisecond timing
│   └── captions.vtt               # WebVTT captions
├── thumbnails/
│   ├── thumbnail_1.png            # Concept 1: The Severed Subsea Core
│   ├── thumbnail_2.png            # Concept 2: The Silent Signal
│   └── thumbnail_3.png            # Concept 3: Zero Packets
├── metadata/
│   └── youtube_metadata.json      # Titles, description, chapters, SEO tags
└── reports/
    └── viewer_review.json         # Independent Viewer Quality Score: 92/100
```

---

## 5. Documentation Suite

- [`docs/GITHUB_RESEARCH.md`](docs/GITHUB_RESEARCH.md): Comprehensive survey and evaluation of open-source video/AI repositories.
- [`docs/REPOSITORY_COMPARISON.md`](docs/REPOSITORY_COMPARISON.md): In-depth comparison database of selected candidate tools.
- [`docs/TECH_STACK.md`](docs/TECH_STACK.md): Full architectural specification and storage topology.
- [`docs/LICENSE_AUDIT.md`](docs/LICENSE_AUDIT.md): Open-source license and YouTube commercial monetization compliance audit.
