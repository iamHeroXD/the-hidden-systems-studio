import os
from pathlib import Path

html_code = """<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>THE HIDDEN SYSTEMS | STUDIO ENGINE</title>
  <!-- Tailwind CSS CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  <!-- Lucide Icons -->
  <script src="https://unpkg.com/lucide@latest"></script>
  <script>
    tailwind.config = {
      darkMode: 'class',
      theme: {
        extend: {
          colors: {
            black: '#050507',
            surface: {
              950: '#09090C',
              900: '#101014',
              850: '#16161C',
              800: '#202028',
              700: '#2E2E38',
              600: '#424250'
            },
            crimson: {
              DEFAULT: '#EF4444',
              glow: '#FF2E4D',
              deep: '#991B1B',
              dark: '#450A0A'
            }
          },
          fontFamily: {
            mono: ['JetBrains Mono', 'ui-monospace', 'SFMono-Regular', 'Menlo', 'monospace'],
            sans: ['Inter', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'sans-serif']
          }
        }
      }
    }
  </script>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700&display=swap');
    body {
      background-color: #050507;
      color: #FFFFFF;
      font-family: 'Inter', sans-serif;
    }
    
    /* Neon Red Glow & Glassmorphism */
    .glow-red {
      box-shadow: 0 0 25px -4px rgba(239, 68, 68, 0.45);
    }
    .glow-red-lg {
      box-shadow: 0 0 40px -2px rgba(255, 46, 77, 0.55);
    }
    .glow-border {
      border: 1px solid rgba(239, 68, 68, 0.4);
    }
    .glow-border:hover {
      border-color: rgba(239, 68, 68, 0.9);
      box-shadow: 0 0 15px rgba(239, 68, 68, 0.3);
    }

    /* Animated Grid Scanlines */
    .bg-grid {
      background-size: 32px 32px;
      background-image: 
        linear-gradient(to right, rgba(255, 255, 255, 0.03) 1px, transparent 1px),
        linear-gradient(to bottom, rgba(255, 255, 255, 0.03) 1px, transparent 1px);
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar { width: 4px; height: 4px; }
    ::-webkit-scrollbar-track { background: #09090C; }
    ::-webkit-scrollbar-thumb { background: #2E2E38; border-radius: 2px; }
    ::-webkit-scrollbar-thumb:hover { background: #EF4444; }

    /* Equalizer Animation for Active Voice/Audio Agent */
    @keyframes eqBar {
      0%, 100% { height: 4px; }
      50% { height: 18px; }
    }
    .eq-bar-1 { animation: eqBar 0.8s ease-in-out infinite; }
    .eq-bar-2 { animation: eqBar 0.5s ease-in-out infinite 0.2s; }
    .eq-bar-3 { animation: eqBar 1.1s ease-in-out infinite 0.4s; }
    .eq-bar-4 { animation: eqBar 0.7s ease-in-out infinite 0.1s; }

    /* Subtle Radar Pulse */
    @keyframes radarPulse {
      0% { transform: scale(0.95); opacity: 0.8; }
      50% { transform: scale(1.05); opacity: 0.3; }
      100% { transform: scale(0.95); opacity: 0.8; }
    }
    .radar-pulse { animation: radarPulse 2.5s infinite ease-in-out; }
  </style>
</head>
<body class="h-screen flex flex-col bg-black text-white selection:bg-crimson selection:text-white overflow-hidden bg-grid">

  <!-- ================= TOP NAVIGATION HUD ================= -->
  <header class="h-16 bg-surface-950/90 backdrop-blur-md border-b border-surface-800 px-6 flex items-center justify-between z-30 shrink-0">
    <!-- Brand Monogram -->
    <div class="flex items-center gap-3.5">
      <div class="w-9 h-9 rounded-lg bg-red-600 flex items-center justify-center glow-red font-black text-black text-base tracking-tighter">
        HS
      </div>
      <div>
        <div class="flex items-center gap-2">
          <h1 class="text-xs font-black tracking-widest text-white uppercase font-mono">THE HIDDEN SYSTEMS</h1>
          <span class="px-1.5 py-0.2 rounded text-[9px] font-mono font-bold bg-red-500/10 text-crimson border border-red-500/30">
            PRO STUDIO
          </span>
        </div>
        <p class="text-[10px] text-zinc-400 font-mono">AUTONOMOUS 2D ANIMATED DOCUMENTARY PLATFORM</p>
      </div>
    </div>

    <!-- Live Studio Mode Pill -->
    <div class="flex items-center gap-3">
      <div class="hidden md:flex items-center gap-2 px-3 py-1 rounded-full bg-surface-900 border border-surface-800 text-[11px] font-mono text-zinc-400">
        <span class="w-2 h-2 rounded-full bg-crimson animate-ping" id="status-pulse-dot"></span>
        <span id="studio-status-label" class="text-white font-bold">READY ON-DEMAND</span>
      </div>

      <!-- MASTER RUN BUTTON -->
      <button onclick="triggerMasterProduction()" id="master-start-btn" class="flex items-center gap-2 px-5 py-2.5 rounded-lg bg-red-600 hover:bg-red-500 text-white font-mono font-black text-xs glow-red transition-all transform active:scale-95">
        <i data-lucide="zap" class="w-4 h-4 fill-white"></i>
        <span>START PRODUCTION</span>
      </button>
    </div>
  </header>

  <!-- ================= WORKSPACE BODY ================= -->
  <div class="flex-1 flex overflow-hidden">
    <!-- Minimal Left Nav -->
    <aside class="w-56 bg-surface-950/80 backdrop-blur-md border-r border-surface-800 flex flex-col justify-between p-3 shrink-0">
      <div class="space-y-1 font-mono text-xs" id="nav-container">
        <button onclick="switchTab('studio')" id="tab-btn-studio" class="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-white bg-surface-850 font-semibold border-l-2 border-crimson transition">
          <i data-lucide="cpu" class="w-4 h-4 text-crimson"></i>
          <span>AI Swarm</span>
        </button>
        <button onclick="switchTab('library')" id="tab-btn-library" class="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-zinc-400 hover:text-white hover:bg-surface-900 transition">
          <i data-lucide="play-circle" class="w-4 h-4"></i>
          <span>Video Master</span>
        </button>
        <button onclick="switchTab('storyboard')" id="tab-btn-storyboard" class="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-zinc-400 hover:text-white hover:bg-surface-900 transition">
          <i data-lucide="film" class="w-4 h-4"></i>
          <span>40 Scenes</span>
        </button>
        <button onclick="switchTab('topics')" id="tab-btn-topics" class="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-zinc-400 hover:text-white hover:bg-surface-900 transition">
          <i data-lucide="compass" class="w-4 h-4"></i>
          <span>Topic Radar</span>
        </button>
        <button onclick="switchTab('script')" id="tab-btn-script" class="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-zinc-400 hover:text-white hover:bg-surface-900 transition">
          <i data-lucide="file-text" class="w-4 h-4"></i>
          <span>Script Ledger</span>
        </button>
      </div>

      <!-- Quick Owner Readout -->
      <div class="p-3 bg-surface-900/60 rounded-xl border border-surface-800 text-[10px] font-mono space-y-1.5">
        <div class="text-zinc-500 uppercase tracking-wider">SYSTEM TELEMETRY</div>
        <div class="flex justify-between text-zinc-300">
          <span>CPU:</span>
          <span id="owner-cpu" class="text-white font-bold">--%</span>
        </div>
        <div class="flex justify-between text-zinc-300">
          <span>RAM:</span>
          <span id="owner-ram" class="text-white font-bold">-- GB</span>
        </div>
        <div class="flex justify-between text-zinc-300">
          <span>PIPELINE:</span>
          <span id="owner-pipeline" class="text-crimson font-bold">18 STAGES</span>
        </div>
      </div>
    </aside>

    <!-- Center Stage -->
    <main class="flex-1 overflow-y-auto p-6" id="stage-viewport">
      <!-- Dynamic View Loaded Here -->
    </main>
  </div>

  <!-- Lightbox Modal for 40 Scene Inspection -->
  <div id="scene-modal" class="fixed inset-0 bg-black/90 backdrop-blur-md z-50 hidden flex items-center justify-center p-4">
    <div class="bg-surface-900 border border-surface-700 rounded-2xl max-w-4xl w-full p-6 relative shadow-2xl space-y-4">
      <button onclick="closeModal()" class="absolute top-4 right-4 text-zinc-400 hover:text-white p-1 rounded-lg bg-surface-800 border border-surface-700">
        <i data-lucide="x" class="w-5 h-5"></i>
      </button>
      <div id="modal-body"></div>
    </div>
  </div>

  <!-- Floating Minimal Toast -->
  <div id="toast" class="fixed bottom-6 right-6 px-4 py-2.5 rounded-lg bg-surface-900 border border-crimson text-xs font-mono text-white shadow-2xl transition-all duration-300 opacity-0 pointer-events-none z-50 flex items-center gap-2">
    <span class="w-2 h-2 rounded-full bg-crimson animate-ping"></span>
    <span id="toast-text">Message</span>
  </div>

  <!-- ================= SCRIPTS ================= -->
  <script>
    let activeTab = "studio";
    let state = {
      production: null,
      topics: [],
      logs: [],
      telemetry: null,
      selectedSceneIdx: 0,
      customTopicInput: ""
    };

    const AI_AGENTS = [
      { id: "research", name: "Topic Discovery Agent", role: "Audience Intelligence", icon: "search", stageRange: [0, 2] },
      { id: "script", name: "Documentary Scriptwriter", role: "5-Act Story Architecture", icon: "pen-tool", stageRange: [3, 4] },
      { id: "critic", name: "Retention Critic Agent", role: "Pacing & Score Review", icon: "check-circle", stageRange: [4, 5] },
      { id: "art", name: "2D Vector Illustrator", role: "Hand-Drawn Artwork (40 Scenes)", icon: "palette", stageRange: [5, 8] },
      { id: "voice", name: "Neural Voice Synthesizer", role: "Edge-TTS Master Narration", icon: "mic", stageRange: [8, 10] },
      { id: "anim", name: "Motion & Camera Animator", role: "1080p 30fps Dynamic Camera Moves", icon: "video", stageRange: [10, 12] },
      { id: "audio", name: "Soundtrack & Loudness Mixer", role: "-16 LUFS EBU R128 Balance", icon: "sliders", stageRange: [12, 14] },
      { id: "subtitles", name: "Subtitle Generator", role: "SRT & VTT Sync", icon: "file-text", stageRange: [14, 15] },
      { id: "quality", name: "Quality Auditor", role: "Frame Density & Gamut Verification", icon: "shield-alert", stageRange: [15, 16] },
      { id: "package", name: "YouTube Packaging Agent", role: "3 High-CTR Thumbnails & Metadata", icon: "package", stageRange: [16, 17] }
    ];

    function showToast(msg) {
      const t = document.getElementById("toast");
      const text = document.getElementById("toast-text");
      text.textContent = msg;
      t.style.opacity = "1";
      setTimeout(() => { t.style.opacity = "0"; }, 3200);
    }

    function switchTab(tabId) {
      activeTab = tabId;
      document.querySelectorAll("#nav-container button").forEach(b => {
        b.className = "w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-zinc-400 hover:text-white hover:bg-surface-900 transition";
      });
      const activeBtn = document.getElementById(`tab-btn-${tabId}`);
      if (activeBtn) {
        activeBtn.className = "w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-white bg-surface-850 font-semibold border-l-2 border-crimson transition";
      }
      renderView();
    }

    async function pollState() {
      try {
        const [prodRes, topRes, sysRes, logRes] = await Promise.all([
          fetch("/api/productions"),
          fetch("/api/topics"),
          fetch("/api/system/status"),
          fetch("/api/logs?limit=30")
        ]);

        if (prodRes.ok) {
          const prods = await prodRes.json();
          if (prods.length > 0) state.production = prods[0];
        }
        if (topRes.ok) {
          const tData = await topRes.json();
          state.topics = tData.candidates || [];
        }
        if (sysRes.ok) {
          const sData = await sysRes.json();
          state.telemetry = sData.telemetry;
          if (state.telemetry) {
            document.getElementById("owner-cpu").textContent = `${state.telemetry.cpu_percent.toFixed(0)}%`;
            document.getElementById("owner-ram").textContent = `${state.telemetry.ram_used_gb} / ${state.telemetry.ram_total_gb} GB`;
          }
        }
        if (logRes.ok) state.logs = await logRes.json();

        updateStatusHeader();
        renderView();
      } catch (e) {
        console.error("Poll err:", e);
      }
    }

    function updateStatusHeader() {
      const p = state.production;
      const label = document.getElementById("studio-status-label");
      const dot = document.getElementById("status-pulse-dot");
      if (!p) return;
      if (p.status === "running") {
        label.textContent = "AI TEAM WORKING...";
        label.className = "text-crimson font-black animate-pulse";
        dot.className = "w-2 h-2 rounded-full bg-crimson animate-ping";
      } else if (p.status === "awaiting_approval") {
        label.textContent = "PRODUCTION COMPLETE";
        label.className = "text-white font-bold";
        dot.className = "w-2 h-2 rounded-full bg-white";
      } else {
        label.textContent = "READY ON-DEMAND";
        label.className = "text-white font-bold";
        dot.className = "w-2 h-2 rounded-full bg-zinc-500";
      }
    }

    async function triggerMasterProduction() {
      const btn = document.getElementById("master-start-btn");
      btn.disabled = true;
      btn.innerHTML = `<i data-lucide="loader-2" class="w-4 h-4 animate-spin text-white"></i><span>INITIALIZING...</span>`;
      lucide.createIcons();
      showToast("Master Production Triggered! Deploying Autonomous AI Team...");
      try {
        await fetch("/api/automation/trigger-now", { method: "POST" });
        switchTab("studio");
        await pollState();
      } catch (err) {
        showToast("Error: " + err.message);
      } finally {
        btn.disabled = false;
        btn.innerHTML = `<i data-lucide="zap" class="w-4 h-4 fill-white"></i><span>START PRODUCTION</span>`;
        lucide.createIcons();
      }
    }

    async function produceTopic(title) {
      showToast(`Building documentary: "${title}"`);
      await fetch("/api/topics/produce", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title })
      });
      switchTab("studio");
      await pollState();
    }

    function copyClip(txt, label) {
      navigator.clipboard.writeText(txt);
      showToast(`Copied ${label} to clipboard!`);
    }

    function openSceneModal(idx) {
      state.selectedSceneIdx = idx;
      renderSceneModalContent();
      document.getElementById("scene-modal").classList.remove("hidden");
      lucide.createIcons();
    }

    function closeModal() {
      document.getElementById("scene-modal").classList.add("hidden");
    }

    function nextScene(delta) {
      const scenes = (state.production && state.production.data && state.production.data.scenes) || [];
      const total = scenes.length || 40;
      state.selectedSceneIdx = (state.selectedSceneIdx + delta + total) % total;
      renderSceneModalContent();
      lucide.createIcons();
    }

    function renderSceneModalContent() {
      const p = state.production || {};
      const scenes = (p.data && p.data.scenes) || [];
      const s = scenes[state.selectedSceneIdx] || {};
      const scNum = (state.selectedSceneIdx + 1).toString().padStart(2, "0");
      const body = document.getElementById("modal-body");
      body.innerHTML = `
        <div class="space-y-4">
          <div class="flex items-center justify-between pr-8">
            <div class="flex items-center gap-3">
              <span class="px-2.5 py-1 rounded bg-red-600 text-white font-mono font-bold text-xs">
                SCENE ${scNum} / ${scenes.length || 40}
              </span>
              <span class="text-xs font-mono text-zinc-400">CAMERA: <span class="text-white font-bold">${s.camera_movement || 'Dynamic Pan'}</span></span>
            </div>
            <div class="flex items-center gap-2">
              <button onclick="nextScene(-1)" class="px-3 py-1 bg-surface-800 hover:bg-surface-700 text-xs font-mono rounded text-white">PREV</button>
              <button onclick="nextScene(1)" class="px-3 py-1 bg-surface-800 hover:bg-surface-700 text-xs font-mono rounded text-white">NEXT</button>
            </div>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div class="bg-black rounded-xl overflow-hidden border border-surface-800">
              <img src="/media/${p.date_folder}/${p.topic_slug}/illustrations/scene_${scNum}.png" class="w-full aspect-video object-cover" />
              <div class="p-1.5 text-center text-[10px] font-mono text-zinc-400 bg-surface-950 border-t border-surface-800">1080P COMPANION RASTER</div>
            </div>
            <div class="bg-black rounded-xl overflow-hidden border border-surface-800">
              <img src="/media/${p.date_folder}/${p.topic_slug}/illustrations/scene_${scNum}.svg" class="w-full aspect-video object-contain p-2" />
              <div class="p-1.5 text-center text-[10px] font-mono text-zinc-400 bg-surface-950 border-t border-surface-800">EDITORIAL VECTOR SVG</div>
            </div>
          </div>
          <div class="bg-surface-950 p-4 rounded-xl border border-surface-800 text-xs space-y-1.5">
            <span class="text-crimson font-mono font-bold block">NARRATION VOICE-OVER (${s.duration_sec || 18}s):</span>
            <p class="text-zinc-200 text-sm leading-relaxed">"${s.narration_chunk || ''}"</p>
          </div>
        </div>
      `;
    }

    function renderView() {
      const v = document.getElementById("stage-viewport");
      const p = state.production || {};
      const pData = p.data || {};
      const scenes = pData.scenes || [];
      const meta = pData.metadata || {};
      const thumbnails = pData.thumbnails || [];
      const script = pData.script || {};

      if (activeTab === "studio") {
        const currentStageIdx = p.current_stage_index || (p.status === "awaiting_approval" ? 18 : 0);
        const isRunning = p.status === "running";

        v.innerHTML = `
          <div class="space-y-6 max-w-6xl mx-auto">
            <!-- Active Production Billboard -->
            <div class="bg-surface-950 border border-surface-800 rounded-2xl p-6 glow-border relative overflow-hidden">
              <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-4">
                <div class="space-y-1">
                  <div class="flex items-center gap-2">
                    <span class="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-red-600 text-white">ACTIVE DOCUMENTARY</span>
                    <span class="text-xs font-mono text-zinc-400">12.6 MIN RUNTIME  |  40 SCENES</span>
                  </div>
                  <h2 class="text-2xl font-black text-white tracking-tight">${p.topic_title || "Standby - Start Production"}</h2>
                </div>
                <div class="flex items-center gap-3">
                  <button onclick="switchTab('library')" class="px-4 py-2 bg-surface-850 hover:bg-surface-800 border border-surface-700 text-xs font-mono rounded-lg text-white flex items-center gap-1.5">
                    <i data-lucide="play" class="w-3.5 h-3.5 text-crimson"></i>
                    <span>WATCH FULL MASTER</span>
                  </button>
                  <a href="/api/productions/${p.id}/export-zip" class="px-4 py-2 bg-red-600 hover:bg-red-500 font-mono font-bold text-xs rounded-lg text-white flex items-center gap-1.5 glow-red">
                    <i data-lucide="download" class="w-3.5 h-3.5"></i>
                    <span>DOWNLOAD .ZIP</span>
                  </a>
                </div>
              </div>

              <!-- Pipeline Progress Gauge -->
              <div class="space-y-1.5">
                <div class="flex justify-between text-xs font-mono">
                  <span class="text-zinc-400">PIPELINE EXECUTION: <span class="text-white font-bold">${p.status ? p.status.toUpperCase() : 'STANDBY'}</span></span>
                  <span class="text-crimson font-bold">${p.progress_pct || 100}%</span>
                </div>
                <div class="w-full h-2 bg-surface-900 rounded-full overflow-hidden border border-surface-800">
                  <div class="h-full bg-gradient-to-r from-red-600 to-crimson-glow transition-all duration-500" style="width: ${p.progress_pct || 100}%"></div>
                </div>
              </div>
            </div>

            <!-- VISUAL AI TEAM SWARM MATRIX -->
            <div>
              <div class="flex items-center justify-between mb-3 font-mono">
                <span class="text-xs font-bold text-zinc-400 uppercase tracking-wider flex items-center gap-2">
                  <span class="w-2 h-2 rounded-full bg-crimson"></span>
                  AUTONOMOUS AI WORKFORCE (10 ACTIVE AGENTS)
                </span>
                <span class="text-[11px] text-zinc-500">REAL-TIME COLLABORATIVE PIPELINE</span>
              </div>

              <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-3.5">
                ${AI_AGENTS.map(agent => {
                  const isActive = isRunning && (currentStageIdx >= agent.stageRange[0] && currentStageIdx <= agent.stageRange[1]);
                  const isDone = currentStageIdx > agent.stageRange[1] || p.status === "awaiting_approval";

                  return `
                    <div class="p-4 rounded-xl border transition-all ${
                      isActive 
                        ? 'bg-surface-900 border-crimson glow-red scale-[1.02]' 
                        : isDone 
                        ? 'bg-surface-950/70 border-surface-800' 
                        : 'bg-surface-950/40 border-surface-850 opacity-40'
                    }">
                      <div class="flex items-center justify-between mb-3">
                        <div class="w-8 h-8 rounded-lg flex items-center justify-center ${isActive ? 'bg-red-600 text-white' : isDone ? 'bg-surface-800 text-white' : 'bg-surface-900 text-zinc-600'}">
                          <i data-lucide="${agent.icon}" class="w-4 h-4"></i>
                        </div>
                        ${isActive ? `
                          <div class="flex items-center gap-1">
                            <span class="w-1.5 h-1.5 rounded-full bg-crimson animate-ping"></span>
                            <span class="text-[9px] font-mono text-crimson font-black tracking-widest">ACTIVE</span>
                          </div>
                        ` : isDone ? `
                          <span class="text-[9px] font-mono text-zinc-400 font-bold">DONE</span>
                        ` : `
                          <span class="text-[9px] font-mono text-zinc-600">IDLE</span>
                        `}
                      </div>

                      <div class="text-xs font-bold text-white tracking-tight">${agent.name}</div>
                      <div class="text-[10px] text-zinc-400 font-mono mt-0.5 line-clamp-1">${agent.role}</div>

                      <!-- Agent Activity Visualizer -->
                      <div class="mt-3 pt-2.5 border-t border-surface-800/80 flex items-center justify-between text-[10px] font-mono">
                        ${isActive ? `
                          <div class="flex items-end gap-1 h-4">
                            <span class="w-1 bg-crimson eq-bar-1"></span>
                            <span class="w-1 bg-crimson eq-bar-2"></span>
                            <span class="w-1 bg-crimson eq-bar-3"></span>
                            <span class="w-1 bg-crimson eq-bar-4"></span>
                          </div>
                          <span class="text-crimson font-bold text-[9px]">COMPUTING</span>
                        ` : isDone ? `
                          <span class="text-zinc-500">OUTPUT SECURED</span>
                          <i data-lucide="check" class="w-3.5 h-3.5 text-zinc-400"></i>
                        ` : `
                          <span class="text-zinc-600">STANDBY</span>
                          <span class="text-zinc-700">--</span>
                        `}
                      </div>
                    </div>
                  `;
                }).join("")}
              </div>
            </div>

            <!-- Real-Time Activity Log Terminal -->
            <div class="bg-surface-950 border border-surface-800 rounded-xl p-4 font-mono text-xs">
              <div class="flex items-center justify-between pb-2 mb-2 border-b border-surface-800 text-zinc-400">
                <span class="font-bold flex items-center gap-2">
                  <i data-lucide="terminal" class="w-3.5 h-3.5 text-crimson"></i>
                  SWARM EVENT STREAM
                </span>
                <span class="text-[10px] text-zinc-600">AUTO-SCROLLING</span>
              </div>
              <div class="space-y-1.5 max-h-48 overflow-y-auto">
                ${state.logs.slice(0, 15).map(l => `
                  <div class="flex items-start gap-2.5 text-[11px]">
                    <span class="text-zinc-600 shrink-0">${l.timestamp ? l.timestamp.split('T')[1].split('.')[0] : ''}</span>
                    <span class="px-1 py-0.2 rounded text-[9px] font-bold bg-surface-850 text-crimson shrink-0">${l.stage}</span>
                    <span class="text-zinc-300 truncate">${l.message}</span>
                  </div>
                `).join("")}
              </div>
            </div>
          </div>
        `;
      } else if (activeTab === "library") {
        v.innerHTML = `
          <div class="space-y-6 max-w-5xl mx-auto">
            <div class="flex items-center justify-between">
              <div>
                <h2 class="text-xl font-black text-white uppercase tracking-wider font-mono">MASTER DOCUMENTARY PLAYER</h2>
                <p class="text-xs text-zinc-400 font-mono mt-0.5">Finished 1080p 30fps broadcast-ready MP4.</p>
              </div>
              <div class="flex items-center gap-2">
                <a href="/media/${p.date_folder}/${p.topic_slug}/video/final_1080p.mp4" download class="px-3 py-1.5 rounded bg-surface-850 hover:bg-surface-800 border border-surface-700 text-xs font-mono text-white">
                  DOWNLOAD 1080P (148 MB)
                </a>
                <a href="/api/productions/${p.id}/export-zip" class="px-4 py-1.5 rounded bg-red-600 hover:bg-red-500 font-mono font-bold text-xs text-white glow-red">
                  DOWNLOAD YOUTUBE BUNDLE (.ZIP)
                </a>
              </div>
            </div>

            <!-- Master Player Container -->
            <div class="bg-surface-950 border border-surface-800 rounded-2xl p-4 glow-border">
              <div class="w-full aspect-video bg-black rounded-xl overflow-hidden border border-surface-800 relative mb-4">
                <video id="player" controls class="w-full h-full" src="/media/${p.date_folder}/${p.topic_slug}/video/preview_720p.mp4" poster="/media/${p.date_folder}/${p.topic_slug}/thumbnails/thumbnail_1.png"></video>
              </div>

              <!-- Chapter Seek Buttons -->
              <div class="flex flex-wrap gap-2 mb-4 pt-2 border-t border-surface-800">
                ${(meta.chapters || [
                  { time: "00:00", title: "Silence at 00:00", sec: 0 },
                  { time: "01:45", title: "Hour 1: Signaling Storm", sec: 105 },
                  { time: "03:30", title: "Hour 3: Ghost Register", sec: 210 },
                  { time: "05:15", title: "Hour 6: Giants of Commerce", sec: 315 },
                  { time: "07:05", title: "Hour 12: Grid Islanding", sec: 425 },
                  { time: "08:50", title: "Hour 18: Analog Renaissance", sec: 530 },
                  { time: "10:35", title: "Hour 24: Thundering Herd", sec: 635 },
                  { time: "12:15", title: "Conclusion: Fragility", sec: 735 }
                ]).map(c => `
                  <button onclick="document.getElementById('player').currentTime = ${c.sec}; document.getElementById('player').play();" class="px-2.5 py-1 rounded bg-surface-900 hover:bg-surface-850 border border-surface-800 text-[11px] font-mono text-zinc-300 hover:text-white">
                    <span class="text-crimson font-bold">${c.time}</span> ${c.title}
                  </button>
                `).join("")}
              </div>

              <!-- Metadata 1-Click Copy Bar -->
              <div class="grid grid-cols-1 md:grid-cols-3 gap-3 pt-3 border-t border-surface-800 text-xs font-mono">
                <button onclick="copyClip('${(meta.final_title || p.topic_title).replace(/'/g, "\\'")}', 'Title')" class="p-3 bg-surface-900 hover:bg-surface-850 rounded-xl border border-surface-800 text-left">
                  <span class="text-zinc-500 block text-[10px]">YOUTUBE TITLE</span>
                  <span class="text-white font-bold block truncate mt-1">${meta.final_title || p.topic_title}</span>
                </button>
                <button onclick="copyClip(\`${(meta.description || '').replace(/`/g, '\\`')}\`, 'Description')" class="p-3 bg-surface-900 hover:bg-surface-850 rounded-xl border border-surface-800 text-left">
                  <span class="text-zinc-500 block text-[10px]">DESCRIPTION & CHAPTERS</span>
                  <span class="text-crimson font-bold block mt-1">CLICK TO COPY FULL TEXT</span>
                </button>
                <button onclick="copyClip('${(meta.tags || []).join(', ')}', 'SEO Tags')" class="p-3 bg-surface-900 hover:bg-surface-850 rounded-xl border border-surface-800 text-left">
                  <span class="text-zinc-500 block text-[10px]">SEO TAGS (COMMA SEPARATED)</span>
                  <span class="text-white font-bold block truncate mt-1">${(meta.tags || []).join(', ')}</span>
                </button>
              </div>
            </div>

            <!-- 3 Thumbnails -->
            <div class="space-y-3">
              <span class="text-xs font-mono font-bold text-zinc-400 uppercase tracking-wider block">3 HIGH-CTR THUMBNAILS (1280x720)</span>
              <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                ${thumbnails.map(t => `
                  <div class="bg-surface-950 border border-surface-800 rounded-xl overflow-hidden shadow-lg group">
                    <img src="/media/${p.date_folder}/${p.topic_slug}/thumbnails/thumbnail_${t.id}.png" class="w-full aspect-video object-cover group-hover:scale-105 transition" />
                    <div class="p-3 flex items-center justify-between">
                      <span class="text-xs font-mono text-white font-bold truncate">${t.title}</span>
                      <a href="/media/${p.date_folder}/${p.topic_slug}/thumbnails/thumbnail_${t.id}.png" download class="text-[10px] font-mono text-crimson hover:underline">DOWNLOAD</a>
                    </div>
                  </div>
                `).join("")}
              </div>
            </div>
          </div>
        `;
      } else if (activeTab === "storyboard") {
        v.innerHTML = `
          <div class="space-y-6 max-w-6xl mx-auto">
            <div class="flex items-center justify-between">
              <div>
                <h2 class="text-xl font-black text-white uppercase tracking-wider font-mono">40-SCENE STORYBOARD</h2>
                <p class="text-xs text-zinc-400 font-mono mt-0.5">Click any scene card to open high-resolution Lightbox view.</p>
              </div>
              <span class="text-xs font-mono text-crimson font-bold">40 ORIGINAL ILLUSTRATIONS</span>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3.5">
              ${scenes.map((s, idx) => {
                const scNum = (idx + 1).toString().padStart(2, "0");
                return `
                  <div onclick="openSceneModal(${idx})" class="bg-surface-950 border border-surface-800 hover:border-crimson rounded-xl overflow-hidden cursor-pointer group transition-all">
                    <div class="w-full aspect-video bg-black relative">
                      <img src="/media/${p.date_folder}/${p.topic_slug}/illustrations/scene_${scNum}.png" class="w-full h-full object-cover group-hover:scale-105 transition duration-300" />
                      <div class="absolute top-2 left-2 px-1.5 py-0.5 rounded bg-black/80 text-[9px] font-mono font-bold text-white">
                        #${scNum}
                      </div>
                      <div class="absolute bottom-2 right-2 px-1.5 py-0.5 rounded bg-red-600/90 text-[9px] font-mono text-white font-bold">
                        ${s.duration_sec}s
                      </div>
                    </div>
                    <div class="p-3 space-y-1">
                      <p class="text-xs text-zinc-300 font-sans line-clamp-2">${s.narration_chunk}</p>
                      <div class="text-[10px] font-mono text-crimson pt-1 flex items-center justify-between border-t border-surface-900">
                        <span>${s.camera_movement}</span>
                        <span class="text-zinc-500">INSPECT</span>
                      </div>
                    </div>
                  </div>
                `;
              }).join("")}
            </div>
          </div>
        `;
      } else if (activeTab === "topics") {
        v.innerHTML = `
          <div class="space-y-6 max-w-5xl mx-auto">
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
              <div>
                <h2 class="text-xl font-black text-white uppercase tracking-wider font-mono">TOPIC RADAR (20 OPPORTUNITIES)</h2>
                <p class="text-xs text-zinc-400 font-mono mt-0.5">High-demand digital mystery and infrastructure concepts ranked by algorithmic opportunity.</p>
              </div>
            </div>

            <div class="bg-surface-950 border border-surface-800 rounded-xl overflow-hidden">
              <table class="w-full text-left text-xs font-mono">
                <thead class="bg-surface-900 border-b border-surface-800 text-zinc-400">
                  <tr>
                    <th class="py-3 px-4">SCORE</th>
                    <th class="py-3 px-4">CONCEPT</th>
                    <th class="py-3 px-4">NICHE</th>
                    <th class="py-3 px-4 text-right">ACTION</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-surface-850">
                  ${state.topics.map(t => `
                    <tr class="hover:bg-surface-900/60 transition">
                      <td class="py-3 px-4 text-crimson font-black text-sm">${t.opportunity_score}</td>
                      <td class="py-3 px-4">
                        <span class="text-white font-sans font-bold block">${t.title}</span>
                        <span class="text-[11px] text-zinc-500 line-clamp-1">${t.angle}</span>
                      </td>
                      <td class="py-3 px-4 text-zinc-400">${t.niche}</td>
                      <td class="py-3 px-4 text-right">
                        <button onclick="produceTopic('${t.title.replace(/'/g, "\\'")}')" class="px-3 py-1 rounded bg-red-600 hover:bg-red-500 text-white font-bold text-xs glow-red transition">
                          PRODUCE NOW
                        </button>
                      </td>
                    </tr>
                  `).join("")}
                </tbody>
              </table>
            </div>
          </div>
        `;
      } else if (activeTab === "script") {
        v.innerHTML = `
          <div class="space-y-6 max-w-4xl mx-auto">
            <div class="flex items-center justify-between">
              <div>
                <h2 class="text-xl font-black text-white uppercase tracking-wider font-mono">5-ACT DOCUMENTARY SCRIPT</h2>
                <p class="text-xs text-zinc-400 font-mono mt-0.5">Engineered for viewer retention and calibrated for 12.6-minute narrative delivery.</p>
              </div>
              <button onclick="copyClip(document.getElementById('script-container').innerText, 'Script')" class="px-3 py-1.5 rounded bg-surface-850 hover:bg-surface-800 border border-surface-700 text-xs font-mono text-white">
                COPY SCRIPT
              </button>
            </div>

            <div class="bg-surface-950 border border-surface-800 rounded-xl p-6 space-y-6 font-mono" id="script-container">
              <div>
                <span class="text-xs text-crimson font-bold">TITLE:</span>
                <h3 class="text-xl font-bold text-white mt-1">${script.title || p.topic_title}</h3>
                <p class="text-xs text-zinc-400 mt-1">${script.logline || ""}</p>
              </div>

              <div class="space-y-4">
                ${(script.acts || []).map(act => `
                  <div class="p-4 rounded-xl bg-surface-900 border border-surface-800 space-y-2">
                    <div class="flex justify-between items-center">
                      <span class="text-xs font-bold text-crimson">ACT ${act.act_number}: ${act.title}</span>
                      <span class="text-[10px] text-zinc-500">~${act.target_duration_sec}s</span>
                    </div>
                    <p class="text-xs text-zinc-300 font-sans leading-relaxed whitespace-pre-wrap">${act.narration_text || ""}</p>
                  </div>
                `).join("")}
              </div>
            </div>
          </div>
        `;
      }

      lucide.createIcons();
    }

    // Startup
    pollState();
    setInterval(pollState, 3000);
  </script>
</body>
</html>
"""

# Write to both template directories
for path_str in ["backend/app/templates/index.html", "backend/templates/index.html"]:
    p = Path(path_str)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(html_code, encoding="utf-8")
    print(f"Updated {path_str} with clean Black/White/Red Minimalist UI & AI Swarm Visualizer.")
