# Repository Comparison Database

This document details the vetted open-source repositories evaluated and integrated into **The Hidden Systems Studio**.

---

## 1. Motion Canvas
- **GitHub URL**: `https://github.com/motion-canvas/motion-canvas`
- **Purpose**: Programmatic 2D vector animation, camera movements, text reveal, and visual timing engine.
- **License**: MIT
- **Installation Method**: `npm install @motion-canvas/core @motion-canvas/2d @motion-canvas/vite-plugin`
- **Dependencies**: Node.js >= 18, Vite, TypeScript
- **Required Hardware**: Any standard modern CPU (GPU acceleration via WebGL/Canvas in headless browser/Puppeteer or node canvas export).
- **API Requirements**: None. Completely local and offline.
- **Integration Method**: Node.js CLI rendering pipeline; project generation via TypeScript templates, rendered to frame sequences or WebM/MP4 via headless worker.
- **Advantages**:
  - Declarative TSX syntax makes scene generation deterministic and scriptable by AI agents.
  - Built-in signals, tweening, and reactive state eliminate manual keyframing errors.
  - Native support for audio synchronization and custom vector shaders.
- **Limitations**:
  - Headless rendering requires Node/Puppeteer or Chrome for batch export.

---

## 2. Rough.js
- **GitHub URL**: `https://github.com/rough-stuff/rough`
- **Purpose**: Procedural hand-drawn, organic, sketchy 2D vector rendering for illustrations, charts, and diagrams.
- **License**: MIT
- **Installation Method**: `npm install roughjs`
- **Dependencies**: Node.js / Browser SVG/Canvas API
- **Required Hardware**: Minimal (runs on any standard CPU).
- **API Requirements**: None.
- **Integration Method**: Integrated into Motion Canvas scenes and the Studio's SVG generator engine.
- **Advantages**:
  - Converts rigid shapes, polygons, and paths into warm, hand-drawn editorial art.
  - Consistent seedable randomness ensures character and diagram linework stability.
  - Perfectly matches the "art-directed hand-drawn 2D explainer" aesthetic.
- **Limitations**:
  - Heavy complex paths with thousands of points can slow down rendering if unoptimized.

---

## 3. Kokoro-ONNX
- **GitHub URL**: `https://github.com/thewh1teagle/kokoro-onnx`
- **Purpose**: Local high-fidelity neural Text-to-Speech (TTS) for documentary narration.
- **License**: Apache-2.0 (weights: Apache-2.0)
- **Installation Method**: `pip install kokoro-onnx soundfile onnxruntime`
- **Dependencies**: Python 3.9+, ONNX Runtime, SoundFile
- **Required Hardware**: Multi-core CPU or lightweight CUDA GPU. Model size is only 82M parameters.
- **API Requirements**: None. 100% offline and free.
- **Integration Method**: Python sub-service inside the Voice Studio agent.
- **Advantages**:
  - Exceptional documentary voice quality comparable to ElevenLabs at zero marginal cost.
  - Extremely fast inference on standard CPU.
  - Multiple distinct narrator personas (`am_adam`, `af_sarah`, `bm_george`, etc.).
- **Limitations**:
  - Requires pre-downloading model file (`kokoro-v1.0.onnx` ~320MB) and voice binaries.

---

## 4. Faster-Whisper
- **GitHub URL**: `https://github.com/SYSTRAN/faster-whisper`
- **Purpose**: Automatic speech recognition, word-level audio synchronization, and SRT/VTT subtitle generation.
- **License**: MIT
- **Installation Method**: `pip install faster-whisper`
- **Dependencies**: CTranslate2, huggingface_hub, Python
- **Required Hardware**: CPU (int8) or GPU (float16). Runs smoothly on CPU for standard audio clips.
- **API Requirements**: None.
- **Integration Method**: Python transcription adapter called after narration rendering.
- **Advantages**:
  - Up to 4x faster than vanilla OpenAI Whisper with significantly lower memory footprint.
  - Millisecond-accurate word boundaries for exact subtitle synchronization.
  - Robust against background audio noise.
- **Limitations**:
  - Initial model download (~140MB for `base` or ~460MB for `small`).

---

## 5. FFmpeg
- **GitHub URL**: `https://github.com/FFmpeg/FFmpeg`
- **Purpose**: Lossless video compositing, multi-track audio mixing, loudness normalization (`EBU R128`), and MP4 muxing.
- **License**: LGPL 2.1+ / GPL 2.0+ (depending on build options)
- **Installation Method**: Pre-installed on host (`ffmpeg version 9.0.2` verified).
- **Dependencies**: None (self-contained native binary).
- **Required Hardware**: CPU (x86_64), optional NVENC/AMF/QSV hardware acceleration.
- **API Requirements**: None.
- **Integration Method**: Subprocess execution with strict JSON/filtergraph arguments and stderr progress parsing.
- **Advantages**:
  - Universal standard for video production; rock-solid reliability.
  - Advanced audio filter graphs: `loudnorm`, `sidechaincompress`, `amerge`, `apad`.
  - Native subtitle burn-in (`subtitles=...`).
- **Limitations**:
  - Complex command-line syntax requires clean wrapper abstraction.

---

## 6. ViMax (Architecture Reference)
- **GitHub URL**: `https://github.com/HKUDS/ViMax`
- **Purpose**: Multi-agent video production orchestration framework (Screenwriter, Storyboarder, Character Consistency, Producer review).
- **License**: Apache-2.0
- **Installation Method**: Architectural pattern adaptation; native Python orchestration agents in Hidden Systems Studio.
- **Dependencies**: Python, Pydantic, LLM client
- **Required Hardware**: Standard CPU.
- **API Requirements**: Gemini API or local Ollama/vLLM endpoints.
- **Integration Method**: Core orchestration pipeline in `backend/app/agents/`.
- **Advantages**:
  - Robust decomposition of 15-minute documentaries into structured acts, scenes, and visual prompts.
  - Structured critic feedback loops prevent narrative drift.
- **Limitations**:
  - The upstream repo is oriented towards text-to-video clips rather than programmatic 2D vector animation. We adapt its multi-agent intelligence to drive Motion Canvas + SVG.

---

## 7. OpenMontage
- **GitHub URL**: `https://github.com/calesthio/OpenMontage`
- **Purpose**: Agentic pipeline architecture, manifest schema, and modular tool design.
- **License**: MIT
- **Installation Method**: Architectural pattern adaptation.
- **Dependencies**: Node.js, Python, FFmpeg
- **Required Hardware**: Any standard PC.
- **API Requirements**: Modular LLM/TTS keys or local fallback.
- **Integration Method**: Project folder manifests (`manifest.json`) and checkpoint recovery.
- **Advantages**:
  - Clean state persistence; enables resuming from interrupted stages.
  - Explicit file-based manifests make debugging simple and auditable.
- **Limitations**:
  - Upstream focuses heavily on archival stock footage rather than custom 2D animated illustrations.

---

## 8. yt-dlp
- **GitHub URL**: `https://github.com/yt-dlp/yt-dlp`
- **Purpose**: YouTube competitor analysis, view velocity tracking, transcript extraction, and metadata mining.
- **License**: The Unlicense (Public Domain)
- **Installation Method**: `pip install yt-dlp`
- **Dependencies**: Python
- **Required Hardware**: Minimal.
- **API Requirements**: None (uses public YouTube endpoints without API key quota limits).
- **Integration Method**: Python adapter in `backend/app/tools/youtube_research.py`.
- **Advantages**:
  - Extracts accurate view counts, upload dates, channel subscriber estimates, and titles for competition scoring.
  - Bypasses strict Google Cloud YouTube API quota limits (10,000 units/day).
- **Limitations**:
  - Frequent YouTube layout changes require pinning or regular library updates.

---

## 9. Manim (Community Edition)
- **GitHub URL**: `https://github.com/ManimCommunity/manim`
- **Purpose**: Programmatic scientific and mathematical vector animations.
- **License**: MIT
- **Installation Method**: `pip install manim`
- **Dependencies**: Python, Cairo, Pango, FFmpeg
- **Required Hardware**: CPU / optional GPU.
- **API Requirements**: None.
- **Integration Method**: Modular scene generator adapter in `backend/app/adapters/manim_adapter.py`.
- **Advantages**:
  - Unequalled for complex algorithmic trees, network packet visualizations, and mathematical physics concepts.
- **Limitations**:
  - Higher system dependencies (Pango/Cairo on Windows); used selectively for specialized technical scenes.

---

## 10. Remotion
- **GitHub URL**: `https://github.com/remotion-dev/remotion`
- **Purpose**: React-based video composition and transition layering.
- **License**: Remotion License
- **Installation Method**: `npm install remotion @remotion/cli`
- **Dependencies**: Node.js, React
- **Required Hardware**: Standard modern CPU.
- **API Requirements**: None.
- **Integration Method**: Secondary compositor for composite overlays and web-based UI scenes.
- **Advantages**:
  - Vast ecosystem of React UI components and web fonts.
- **Limitations**:
  - Commercial license restrictions for companies with >$3M ARR (individual/educational use is unrestricted).
