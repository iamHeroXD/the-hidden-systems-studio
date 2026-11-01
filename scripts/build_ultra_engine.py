import os
from pathlib import Path

html_content = """<!DOCTYPE html>
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
            black: '#000000',
            surface: {
              950: '#060608',
              900: '#0C0C10',
              850: '#14141A',
              800: '#1C1C24',
              700: '#282834',
              600: '#3A3A4A'
            },
            crimson: {
              DEFAULT: '#EF4444',
              glow: '#FF2A4A',
              dark: '#991B1B'
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
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@500;700&display=swap');
    body {
      background-color: #000000;
      color: #FFFFFF;
      font-family: 'Inter', sans-serif;
    }
    
    .glow-red {
      box-shadow: 0 0 25px -2px rgba(239, 68, 68, 0.45);
    }
    .glow-red-lg {
      box-shadow: 0 0 45px 0px rgba(255, 42, 74, 0.55);
    }
    .border-glow {
      border: 1px solid rgba(239, 68, 68, 0.35);
    }
    .border-glow:hover {
      border-color: #EF4444;
      box-shadow: 0 0 16px rgba(239, 68, 68, 0.35);
    }

    .bg-grid {
      background-size: 40px 40px;
      background-image: 
        linear-gradient(to right, rgba(255, 255, 255, 0.02) 1px, transparent 1px),
        linear-gradient(to bottom, rgba(255, 255, 255, 0.02) 1px, transparent 1px);
    }

    ::-webkit-scrollbar { width: 4px; height: 4px; }
    ::-webkit-scrollbar-track { background: #060608; }
    ::-webkit-scrollbar-thumb { background: #282834; border-radius: 2px; }
    ::-webkit-scrollbar-thumb:hover { background: #EF4444; }

    @keyframes eqBar {
      0%, 100% { height: 3px; }
      50% { height: 16px; }
    }
    .eq-1 { animation: eqBar 0.7s ease-in-out infinite; }
    .eq-2 { animation: eqBar 0.4s ease-in-out infinite 0.15s; }
    .eq-3 { animation: eqBar 0.9s ease-in-out infinite 0.3s; }
    .eq-4 { animation: eqBar 0.6s ease-in-out infinite 0.05s; }
  </style>
</head>
<body class="h-screen flex flex-col bg-black text-white selection:bg-crimson selection:text-white overflow-hidden bg-grid">

  <!-- ================= TOP HUD HEADER ================= -->
  <header class="h-16 bg-surface-950/90 backdrop-blur-md border-b border-surface-800 px-6 flex items-center justify-between shrink-0 z-30">
    <!-- Brand -->
    <div class="flex items-center gap-3">
      <div class="w-9 h-9 rounded-lg bg-red-600 flex items-center justify-center font-black text-black text-sm glow-red tracking-tighter">
        HS
      </div>
      <div>
        <div class="flex items-center gap-2">
          <h1 class="text-xs font-black tracking-widest text-white uppercase font-mono">THE HIDDEN SYSTEMS</h1>
          <span class="px-1.5 py-0.5 rounded text-[9px] font-mono font-bold bg-red-600/20 text-crimson border border-red-600/40">
            PRO STUDIO
          </span>
        </div>
        <p class="text-[10px] text-zinc-500 font-mono">AUTONOMOUS 2D ANIMATED DOCUMENTARY PLATFORM</p>
      </div>
    </div>

    <!-- Live Status & Instant Trigger -->
    <div class="flex items-center gap-4">
      <div class="hidden sm:flex items-center gap-2 px-3 py-1 rounded-full bg-surface-900 border border-surface-800 text-[11px] font-mono">
        <span class="w-2 h-2 rounded-full bg-crimson animate-ping" id="status-dot"></span>
        <span id="status-label" class="text-zinc-300 font-bold uppercase">STANDBY</span>
      </div>

      <button onclick="triggerProduction()" id="header-start-btn" class="flex items-center gap-2 px-5 py-2.5 rounded-lg bg-red-600 hover:bg-red-500 text-white font-mono font-black text-xs glow-red transition transform active:scale-95">
        <i data-lucide="zap" class="w-4 h-4 fill-white"></i>
        <span>START PRODUCTION</span>
      </button>
    </div>
  </header>

  <!-- ================= MAIN WORKSPACE ================= -->
  <div class="flex-1 flex overflow-hidden">
    <!-- Left Navigation -->
    <aside class="w-56 bg-surface-950/80 backdrop-blur-md border-r border-surface-800 flex flex-col justify-between p-3 shrink-0">
      <div class="space-y-1 font-mono text-xs" id="nav-list">
        <button onclick="selectTab('overview')" id="nav-overview" class="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-white bg-surface-850 font-bold border-l-2 border-crimson transition">
          <i data-lucide="layout-dashboard" class="w-4 h-4 text-crimson"></i>
          <span>Dashboard</span>
        </button>
        <button onclick="selectTab('swarm')" id="nav-swarm" class="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-zinc-400 hover:text-white hover:bg-surface-900 transition">
          <i data-lucide="cpu" class="w-4 h-4"></i>
          <span>AI Swarm (8)</span>
        </button>
        <button onclick="selectTab('video')" id="nav-video" class="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-zinc-400 hover:text-white hover:bg-surface-900 transition">
          <i data-lucide="play-circle" class="w-4 h-4"></i>
          <span>Video Master</span>
        </button>
        <button onclick="selectTab('storyboard')" id="nav-storyboard" class="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-zinc-400 hover:text-white hover:bg-surface-900 transition">
          <i data-lucide="film" class="w-4 h-4"></i>
          <span>40 Scenes</span>
        </button>
        <button onclick="selectTab('topics')" id="nav-topics" class="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-zinc-400 hover:text-white hover:bg-surface-900 transition">
          <i data-lucide="compass" class="w-4 h-4"></i>
          <span>Topic Radar</span>
        </button>
        <button onclick="selectTab('script')" id="nav-script" class="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-zinc-400 hover:text-white hover:bg-surface-900 transition">
          <i data-lucide="file-text" class="w-4 h-4"></i>
          <span>Script</span>
        </button>
      </div>

      <!-- Quick Owner Telemetry HUD -->
      <div class="p-3 bg-surface-900/60 rounded-xl border border-surface-800 text-[10px] font-mono space-y-1.5">
        <div class="text-zinc-500 uppercase tracking-wider font-bold">STUDIO TELEMETRY</div>
        <div class="flex justify-between text-zinc-400">
          <span>CPU:</span>
          <span id="stat-cpu" class="text-white font-bold">--%</span>
        </div>
        <div class="flex justify-between text-zinc-400">
          <span>RAM:</span>
          <span id="stat-ram" class="text-white font-bold">-- / -- GB</span>
        </div>
        <div class="flex justify-between text-zinc-400">
          <span>OUTPUT:</span>
          <span class="text-crimson font-bold">1080P 30FPS</span>
        </div>
      </div>
    </aside>

    <!-- Main Viewport Stage -->
    <main class="flex-1 overflow-y-auto p-6" id="viewport">
      <!-- Dynamic Injected Content -->
    </main>
  </div>

  <!-- Scene Inspection Lightbox Modal -->
  <div id="modal" class="fixed inset-0 bg-black/90 backdrop-blur-md z-50 hidden flex items-center justify-center p-4">
    <div class="bg-surface-900 border border-surface-700 rounded-2xl max-w-4xl w-full p-6 relative shadow-2xl space-y-4">
      <button onclick="closeModal()" class="absolute top-4 right-4 text-zinc-400 hover:text-white p-1 rounded-lg bg-surface-800 border border-surface-700">
        <i data-lucide="x" class="w-5 h-5"></i>
      </button>
      <div id="modal-content"></div>
    </div>
  </div>

  <!-- Minimalist Floating Toast -->
  <div id="toast" class="fixed bottom-6 right-6 px-4 py-2.5 rounded-lg bg-surface-900 border border-crimson text-xs font-mono text-white shadow-2xl transition-all duration-300 opacity-0 pointer-events-none z-50 flex items-center gap-2">
    <span class="w-2 h-2 rounded-full bg-crimson animate-ping"></span>
    <span id="toast-msg">Message</span>
  </div>

  <!-- ================= JAVASCRIPT ================= -->
  <script>
    let currentTab = "overview";
    let state = {
      prod: null,
      progress: null,
      topics: [],
      logs: [],
      telemetry: null,
      sceneIdx: 0,
      countdownTimer: null
    };

    const AI_AGENTS = [
      { id: "director", name: "ORCHESTRATOR AI", role: "Pipeline Director", icon: "activity", stageRange: [0, 1] },
      { id: "research", name: "RESEARCH AI", role: "Fact-Checked Dossier", icon: "search", stageRange: [1, 3] },
      { id: "writer", name: "SCRIPTWRITER AI", role: "5-Act Retention Narrative", icon: "pen-tool", stageRange: [3, 5] },
      { id: "illustrator", name: "ILLUSTRATION AI", role: "40 Vector 1080p Scenes", icon: "palette", stageRange: [5, 8] },
      { id: "voice", name: "NEURAL VOICE AI", role: "Edge-TTS Narration Master", icon: "mic", stageRange: [8, 10] },
      { id: "animator", name: "ANIMATION AI", role: "1080p Camera Movement", icon: "video", stageRange: [10, 12] },
      { id: "sound", name: "MASTER AUDIO AI", role: "EBU R128 -16 LUFS Mixer", icon: "sliders", stageRange: [12, 14] },
      { id: "publisher", name: "YOUTUBE PUBLISHER AI", role: "Thumbnails & Release Package", icon: "package", stageRange: [15, 17] }
    ];

    function showToast(text) {
      const t = document.getElementById("toast");
      document.getElementById("toast-msg").textContent = text;
      t.style.opacity = "1";
      setTimeout(() => { t.style.opacity = "0"; }, 3200);
    }

    function formatTime(sec) {
      if (!sec || sec < 0) sec = 0;
      const m = Math.floor(sec / 60).toString().padStart(2, "0");
      const s = Math.floor(sec % 60).toString().padStart(2, "0");
      return `${m}:${s}`;
    }

    function selectTab(tabId) {
      currentTab = tabId;
      document.querySelectorAll("#nav-list button").forEach(b => {
        b.className = "w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-zinc-400 hover:text-white hover:bg-surface-900 transition";
      });
      const activeBtn = document.getElementById(`nav-${tabId}`);
      if (activeBtn) {
        activeBtn.className = "w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-white bg-surface-850 font-bold border-l-2 border-crimson transition";
      }
      renderView();
    }

    async function pollProgress() {
      try {
        const res = await fetch("/api/progress");
        if (res.ok) {
          const prog = await res.json();
          state.progress = prog;
          updateStatus();
          // If in flight, re-render to keep countdown and micro-bars fluid
          if (prog.status === "running") {
            renderView();
          }
        }
      } catch (e) {
        console.error("Progress poll err:", e);
      }
    }

    async function pollFull() {
      try {
        const [prodRes, topRes, sysRes, logRes] = await Promise.all([
          fetch("/api/productions"),
          fetch("/api/topics"),
          fetch("/api/system/status"),
          fetch("/api/logs?limit=25")
        ]);

        if (prodRes.ok) {
          const prods = await prodRes.json();
          if (prods.length > 0) state.prod = prods[0];
        }
        if (topRes.ok) {
          const t = await topRes.json();
          state.topics = t.candidates || [];
        }
        if (sysRes.ok) {
          const s = await sysRes.json();
          state.telemetry = s.telemetry;
          if (state.telemetry) {
            document.getElementById("stat-cpu").textContent = `${state.telemetry.cpu_percent.toFixed(0)}%`;
            document.getElementById("stat-ram").textContent = `${state.telemetry.ram_used_gb} / ${state.telemetry.ram_total_gb} GB`;
          }
        }
        if (logRes.ok) state.logs = await logRes.json();

        updateStatus();
        renderView();
      } catch (e) {
        console.error("Full poll err:", e);
      }
    }

    function updateStatus() {
      const prog = state.progress;
      const label = document.getElementById("status-label");
      const dot = document.getElementById("status-dot");
      if (!prog) return;

      if (prog.status === "running") {
        label.textContent = `WORKING: STAGE ${prog.stage_index + 1}/18 (${prog.progress_pct}%)`;
        label.className = "text-crimson font-black animate-pulse";
        dot.className = "w-2 h-2 rounded-full bg-crimson animate-ping";
      } else if (prog.status === "awaiting_approval" || prog.status === "completed") {
        label.textContent = "COMPLETE - MASTER READY";
        label.className = "text-white font-bold";
        dot.className = "w-2 h-2 rounded-full bg-white";
      } else {
        label.textContent = "READY ON-DEMAND";
        label.className = "text-zinc-400 font-bold";
        dot.className = "w-2 h-2 rounded-full bg-zinc-600";
      }
    }

    async function triggerProduction() {
      const btn = document.getElementById("header-start-btn");
      btn.disabled = true;
      btn.innerHTML = `<i data-lucide="loader-2" class="w-4 h-4 animate-spin"></i><span>STARTING...</span>`;
      lucide.createIcons();
      showToast("Master Production Deployed! Parallel AI Agents Engaged.");
      try {
        await fetch("/api/automation/trigger-now", { method: "POST" });
        await pollProgress();
        await pollFull();
      } catch (err) {
        showToast("Error: " + err.message);
      } finally {
        btn.disabled = false;
        btn.innerHTML = `<i data-lucide="zap" class="w-4 h-4 fill-white"></i><span>START PRODUCTION</span>`;
        lucide.createIcons();
      }
    }

    async function buildTopic(title) {
      showToast(`Building documentary: "${title}"`);
      await fetch("/api/topics/produce", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title })
      });
      await pollProgress();
      await pollFull();
    }

    function copyToClipboard(text, label) {
      navigator.clipboard.writeText(text);
      showToast(`Copied ${label} to clipboard!`);
    }

    function openModal(idx) {
      state.sceneIdx = idx;
      renderModal();
      document.getElementById("modal").classList.remove("hidden");
      lucide.createIcons();
    }

    function closeModal() {
      document.getElementById("modal").classList.add("hidden");
    }

    function stepScene(delta) {
      const scenes = (state.prod && state.prod.data && state.prod.data.scenes) || [];
      const total = scenes.length || 40;
      state.sceneIdx = (state.sceneIdx + delta + total) % total;
      renderModal();
      lucide.createIcons();
    }

    function renderModal() {
      const p = state.prod || {};
      const scenes = (p.data && p.data.scenes) || [];
      const s = scenes[state.sceneIdx] || {};
      const scNum = (state.sceneIdx + 1).toString().padStart(2, "0");
      const content = document.getElementById("modal-content");
      content.innerHTML = `
        <div class="space-y-4">
          <div class="flex items-center justify-between pr-8">
            <div class="flex items-center gap-3">
              <span class="px-2.5 py-1 rounded bg-red-600 text-white font-mono font-bold text-xs">
                SCENE ${scNum} / ${scenes.length || 40}
              </span>
              <span class="text-xs font-mono text-zinc-400">CAMERA MOVE: <span class="text-white font-bold">${s.camera_movement || 'Dynamic Pan'}</span></span>
            </div>
            <div class="flex items-center gap-2">
              <button onclick="stepScene(-1)" class="px-3 py-1 bg-surface-800 hover:bg-surface-700 text-xs font-mono rounded text-white">PREV</button>
              <button onclick="stepScene(1)" class="px-3 py-1 bg-surface-800 hover:bg-surface-700 text-xs font-mono rounded text-white">NEXT</button>
            </div>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div class="bg-black rounded-xl overflow-hidden border border-surface-800">
              <img src="/media/${p.date_folder}/${p.topic_slug}/illustrations/scene_${scNum}.png" class="w-full aspect-video object-cover" />
              <div class="p-1.5 text-center text-[10px] font-mono text-zinc-400 bg-surface-950 border-t border-surface-800">1080P RASTER FRAME</div>
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
      const v = document.getElementById("viewport");
      const p = state.prod || {};
      const prog = state.progress || {};
      const isRunning = prog.status === "running";
      const currentStageIdx = prog.stage_index !== undefined ? prog.stage_index : (p.current_stage_index || 0);
      const pData = p.data || {};
      const scenes = pData.scenes || [];
      const meta = pData.metadata || {};
      const thumbnails = pData.thumbnails || [];
      const script = pData.script || {};

      if (currentTab === "overview") {
        v.innerHTML = `
          <div class="space-y-6 max-w-6xl mx-auto">
            <!-- LIVE MISSION PROGRESS HUD (VISIBLE WHEN RUNNING) -->
            ${isRunning ? `
              <div class="bg-surface-950 border border-crimson rounded-2xl p-6 glow-red relative overflow-hidden">
                <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-4">
                  <div class="flex items-center gap-3">
                    <span class="w-3 h-3 rounded-full bg-crimson animate-ping"></span>
                    <div>
                      <span class="text-[10px] font-mono text-crimson font-black tracking-widest uppercase">AUTONOMOUS PRODUCTION IN FLIGHT</span>
                      <h3 class="text-lg font-black text-white font-mono mt-0.5">${prog.title || p.topic_title || "Generating Documentary..."}</h3>
                    </div>
                  </div>
                  <div class="flex items-center gap-4 text-right">
                    <div>
                      <span class="text-[10px] font-mono text-zinc-500 block">TIME REMAINING</span>
                      <span class="text-2xl font-black text-crimson font-mono tracking-tight" id="countdown-val">
                        ${formatTime(prog.eta_sec || 45)}
                      </span>
                    </div>
                    <div class="border-l border-surface-800 pl-4">
                      <span class="text-[10px] font-mono text-zinc-500 block">ELAPSED TIME</span>
                      <span class="text-lg font-bold text-white font-mono">
                        ${formatTime(prog.elapsed_sec || 0)}
                      </span>
                    </div>
                  </div>
                </div>

                <!-- Overall Progress Bar -->
                <div class="space-y-1.5 mb-4">
                  <div class="flex justify-between text-xs font-mono">
                    <span class="text-zinc-300 font-bold">
                      STAGE ${prog.stage_index + 1} OF ${prog.total_stages || 18}: 
                      <span class="text-white">${prog.live?.stage_name || (prog.stages && prog.stages[prog.stage_index] ? prog.stages[prog.stage_index].name : 'Executing')}</span>
                    </span>
                    <span class="text-crimson font-black text-sm">${prog.progress_pct || 0}%</span>
                  </div>
                  <div class="w-full h-3 bg-surface-900 rounded-full overflow-hidden border border-surface-800 p-0.5">
                    <div class="h-full bg-gradient-to-r from-red-600 to-crimson-glow rounded-full transition-all duration-300" style="width: ${prog.progress_pct || 0}%"></div>
                  </div>
                </div>

                <!-- Live Micro-Meter -->
                ${prog.live && prog.live.total ? `
                  <div class="bg-surface-900 border border-surface-800 rounded-xl p-3 flex items-center justify-between font-mono text-xs">
                    <div class="flex items-center gap-2">
                      <i data-lucide="activity" class="w-4 h-4 text-crimson"></i>
                      <span class="text-zinc-300 font-bold">${prog.live.msg || 'Processing'}</span>
                    </div>
                    <span class="text-crimson font-black">${prog.live.done || 0} / ${prog.live.total || 40} (${prog.live.pct || 0}%)</span>
                  </div>
                ` : ''}
              </div>
            ` : ''}

            <!-- Command Center Hero -->
            <div class="bg-surface-950 border border-surface-800 rounded-2xl p-6 relative overflow-hidden border-glow">
              <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-6">
                <div class="space-y-2">
                  <div class="flex items-center gap-2">
                    <span class="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-red-600 text-white">AUTONOMOUS ENGINE</span>
                    <span class="text-xs font-mono text-zinc-500">CHANNEL: THE HIDDEN SYSTEMS</span>
                  </div>
                  <h2 class="text-2xl font-black text-white tracking-tight">Instant 1-Click Documentary Engine</h2>
                  <p class="text-xs text-zinc-400 max-w-2xl font-sans">
                    Multi-threaded parallel architecture. Generates 40 custom editorial vector scenes, 5-act retention scripts, 1080p camera motion, and a YouTube-ready release package in ~60 seconds.
                  </p>
                </div>
                <div class="flex items-center gap-3 shrink-0">
                  <button onclick="triggerProduction()" class="px-6 py-3.5 rounded-xl bg-red-600 hover:bg-red-500 text-white font-mono font-black text-xs glow-red transition transform active:scale-95 flex items-center gap-2">
                    <i data-lucide="zap" class="w-4 h-4 fill-white"></i>
                    <span>START PRODUCTION</span>
                  </button>
                  <button onclick="selectTab('video')" class="px-4 py-3.5 rounded-xl bg-surface-850 hover:bg-surface-800 border border-surface-700 text-white font-mono text-xs transition flex items-center gap-2">
                    <i data-lucide="play" class="w-4 h-4 text-crimson"></i>
                    <span>WATCH MASTER</span>
                  </button>
                </div>
              </div>

              <!-- Custom Topic Quick Producer -->
              <div class="mt-6 pt-5 border-t border-surface-800 flex items-center gap-3">
                <input id="quick-input" type="text" placeholder="Type any topic (e.g. 'What If All Satellites Collapsed In A Kessler Syndrome Cascade?')..." class="flex-1 bg-surface-900 border border-surface-800 rounded-lg px-4 py-2.5 text-xs font-sans text-white focus:outline-none focus:border-red-600" />
                <button onclick="const t = document.getElementById('quick-input').value; if(t) buildTopic(t); else showToast('Enter a topic first.');" class="px-4 py-2.5 rounded-lg bg-surface-850 hover:bg-surface-800 border border-surface-700 text-crimson font-mono font-bold text-xs">
                  BUILD THIS TOPIC
                </button>
              </div>
            </div>

            <!-- Master Video Monitor Card -->
            <div class="bg-surface-950 border border-surface-800 rounded-2xl p-5 border-glow">
              <div class="flex items-center justify-between mb-3">
                <span class="text-xs font-mono font-bold text-white uppercase tracking-wider flex items-center gap-2">
                  <span class="w-2 h-2 rounded-full bg-crimson animate-pulse"></span>
                  LATEST FINISHED DOCUMENTARY MASTER
                </span>
                <div class="flex items-center gap-2">
                  <a href="/media/${p.date_folder}/${p.topic_slug}/video/final_1080p.mp4" download class="px-3 py-1 bg-surface-900 hover:bg-surface-850 border border-surface-800 text-[11px] font-mono rounded text-zinc-300">
                    DOWNLOAD 1080P
                  </a>
                  <a href="/api/productions/${p.id}/export-zip" class="px-3.5 py-1 bg-red-600 hover:bg-red-500 text-white font-mono font-bold text-[11px] rounded glow-red">
                    DOWNLOAD .ZIP PACKAGE
                  </a>
                </div>
              </div>

              <div class="w-full aspect-video bg-black rounded-xl overflow-hidden border border-surface-800 mb-3 relative">
                <video id="master-vid" controls class="w-full h-full" src="/media/${p.date_folder}/${p.topic_slug}/video/preview_720p.mp4" poster="/media/${p.date_folder}/${p.topic_slug}/thumbnails/thumbnail_1.png"></video>
              </div>

              <div class="flex flex-wrap gap-2 pt-2 border-t border-surface-800/80">
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
                  <button onclick="document.getElementById('master-vid').currentTime = ${c.sec}; document.getElementById('master-vid').play();" class="px-2.5 py-1 rounded bg-surface-900 hover:bg-surface-850 border border-surface-800 text-[11px] font-mono text-zinc-300">
                    <span class="text-crimson font-bold">${c.time}</span> ${c.title}
                  </button>
                `).join("")}
              </div>
            </div>

            <!-- Stats Bar -->
            <div class="grid grid-cols-2 md:grid-cols-4 gap-3.5">
              <div class="bg-surface-950 border border-surface-800 rounded-xl p-4">
                <span class="text-[10px] font-mono text-zinc-500 block">DOCUMENTARY RUNTIME</span>
                <span class="text-lg font-bold text-white font-mono mt-1 block">12.6 Minutes</span>
              </div>
              <div class="bg-surface-950 border border-surface-800 rounded-xl p-4">
                <span class="text-[10px] font-mono text-zinc-500 block">SCENE ASSETS</span>
                <span class="text-lg font-bold text-crimson font-mono mt-1 block">40 Scenes</span>
              </div>
              <div class="bg-surface-950 border border-surface-800 rounded-xl p-4">
                <span class="text-[10px] font-mono text-zinc-500 block">QUALITY GATE</span>
                <span class="text-lg font-bold text-white font-mono mt-1 block">${p.review_score || 94} / 100</span>
              </div>
              <div class="bg-surface-950 border border-surface-800 rounded-xl p-4">
                <span class="text-[10px] font-mono text-zinc-500 block">ENGINE STATUS</span>
                <span class="text-lg font-bold text-white font-mono mt-1 block">${prog.status ? prog.status.toUpperCase() : 'STANDBY'}</span>
              </div>
            </div>
          </div>
        `;
      } else if (currentTab === "swarm") {
        v.innerHTML = `
          <div class="space-y-6 max-w-6xl mx-auto">
            <div class="flex items-center justify-between">
              <div>
                <h2 class="text-xl font-black text-white uppercase tracking-wider font-mono">AUTONOMOUS AI SWARM MATRIX</h2>
                <p class="text-xs text-zinc-400 font-mono mt-0.5">8 specialized neural agents collaborating across the 18-stage pipeline.</p>
              </div>
              <button onclick="triggerProduction()" class="px-4 py-2 bg-red-600 hover:bg-red-500 text-white font-mono font-bold text-xs rounded-lg glow-red">
                DEPLOY ALL AGENTS
              </button>
            </div>

            <!-- Progress Bar -->
            <div class="bg-surface-950 border border-surface-800 rounded-xl p-4">
              <div class="flex justify-between text-xs font-mono mb-2">
                <span class="text-zinc-400">PIPELINE COMPLETION:</span>
                <span class="text-crimson font-bold">${prog.progress_pct || p.progress_pct || 100}%</span>
              </div>
              <div class="w-full h-2 bg-surface-900 rounded-full overflow-hidden border border-surface-800">
                <div class="h-full bg-gradient-to-r from-red-600 to-crimson-glow transition-all duration-300" style="width: ${prog.progress_pct || p.progress_pct || 100}%"></div>
              </div>
            </div>

            <!-- 8 AI Agents Grid -->
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              ${AI_AGENTS.map(agent => {
                const isActive = isRunning && (currentStageIdx >= agent.stageRange[0] && currentStageIdx <= agent.stageRange[1]);
                const isDone = currentStageIdx > agent.stageRange[1] || prog.status === "awaiting_approval" || prog.status === "completed";

                return `
                  <div class="p-4 rounded-xl border transition-all ${
                    isActive 
                      ? 'bg-surface-900 border-crimson glow-red scale-[1.02]' 
                      : isDone 
                      ? 'bg-surface-950 border-surface-800' 
                      : 'bg-surface-950/40 border-surface-850 opacity-40'
                  }">
                    <div class="flex items-center justify-between mb-3">
                      <div class="w-9 h-9 rounded-lg flex items-center justify-center ${isActive ? 'bg-red-600 text-white' : isDone ? 'bg-surface-800 text-white' : 'bg-surface-900 text-zinc-600'}">
                        <i data-lucide="${agent.icon}" class="w-4 h-4"></i>
                      </div>
                      ${isActive ? `
                        <div class="flex items-center gap-1.5">
                          <span class="w-2 h-2 rounded-full bg-crimson animate-ping"></span>
                          <span class="text-[9px] font-mono text-crimson font-black tracking-widest">WORKING</span>
                        </div>
                      ` : isDone ? `
                        <span class="text-[9px] font-mono text-white font-bold bg-surface-850 px-2 py-0.5 rounded border border-surface-700">DONE</span>
                      ` : `
                        <span class="text-[9px] font-mono text-zinc-600">STANDBY</span>
                      `}
                    </div>

                    <div class="text-xs font-bold text-white font-mono tracking-tight">${agent.name}</div>
                    <div class="text-[10px] text-zinc-400 font-sans mt-0.5">${agent.role}</div>

                    <!-- Animated Agent Visualizer -->
                    <div class="mt-4 pt-3 border-t border-surface-800/80 flex items-center justify-between text-[10px] font-mono">
                      ${isActive ? `
                        <div class="flex items-end gap-1 h-3.5">
                          <span class="w-1 bg-crimson eq-1"></span>
                          <span class="w-1 bg-crimson eq-2"></span>
                          <span class="w-1 bg-crimson eq-3"></span>
                          <span class="w-1 bg-crimson eq-4"></span>
                        </div>
                        <span class="text-crimson font-bold">ACTIVE</span>
                      ` : isDone ? `
                        <span class="text-zinc-500">COMPLETE</span>
                        <i data-lucide="check" class="w-3.5 h-3.5 text-zinc-400"></i>
                      ` : `
                        <span class="text-zinc-600">IDLE</span>
                        <span class="text-zinc-700">--</span>
                      `}
                    </div>
                  </div>
                `;
              }).join("")}
            </div>

            <!-- Terminal Log Stream -->
            <div class="bg-surface-950 border border-surface-800 rounded-xl p-4 font-mono text-xs">
              <div class="flex items-center justify-between pb-2 mb-2 border-b border-surface-800 text-zinc-400">
                <span class="font-bold flex items-center gap-2">
                  <i data-lucide="terminal" class="w-3.5 h-3.5 text-crimson"></i>
                  SWARM LOG STREAM
                </span>
                <span class="text-[10px] text-zinc-600">LIVE SYNC</span>
              </div>
              <div class="space-y-1.5 max-h-48 overflow-y-auto">
                ${state.logs.slice(0, 15).map(l => `
                  <div class="flex items-start gap-2.5 text-[11px]">
                    <span class="text-zinc-600 shrink-0">${l.timestamp ? l.timestamp.split('T')[1].split('.')[0] : ''}</span>
                    <span class="px-1.5 py-0.2 rounded text-[9px] font-bold bg-surface-850 text-crimson shrink-0">${l.stage}</span>
                    <span class="text-zinc-300 truncate">${l.message}</span>
                  </div>
                `).join("")}
              </div>
            </div>
          </div>
        `;
      } else if (currentTab === "video") {
        v.innerHTML = `
          <div class="space-y-6 max-w-5xl mx-auto">
            <div class="flex items-center justify-between">
              <div>
                <h2 class="text-xl font-black text-white uppercase tracking-wider font-mono">MASTER VIDEO DECK</h2>
                <p class="text-xs text-zinc-400 font-mono mt-0.5">Broadcast-grade 1080p MP4 master with YouTube metadata package.</p>
              </div>
              <div class="flex items-center gap-2">
                <a href="/media/${p.date_folder}/${p.topic_slug}/video/final_1080p.mp4" download class="px-3 py-1.5 rounded bg-surface-850 hover:bg-surface-800 border border-surface-700 text-xs font-mono text-white">
                  DOWNLOAD 1080P MASTER
                </a>
                <a href="/api/productions/${p.id}/export-zip" class="px-4 py-1.5 rounded bg-red-600 hover:bg-red-500 font-mono font-bold text-xs text-white glow-red">
                  DOWNLOAD .ZIP PACKAGE
                </a>
              </div>
            </div>

            <!-- Master Player -->
            <div class="bg-surface-950 border border-surface-800 rounded-2xl p-4 border-glow">
              <div class="w-full aspect-video bg-black rounded-xl overflow-hidden border border-surface-800 relative mb-4">
                <video id="player" controls class="w-full h-full" src="/media/${p.date_folder}/${p.topic_slug}/video/preview_720p.mp4" poster="/media/${p.date_folder}/${p.topic_slug}/thumbnails/thumbnail_1.png"></video>
              </div>

              <!-- Metadata 1-Click Copy Bar -->
              <div class="grid grid-cols-1 md:grid-cols-3 gap-3 pt-3 border-t border-surface-800 text-xs font-mono">
                <button onclick="copyToClipboard('${(meta.final_title || p.topic_title).replace(/'/g, "\\'")}', 'Title')" class="p-3 bg-surface-900 hover:bg-surface-850 rounded-xl border border-surface-800 text-left">
                  <span class="text-zinc-500 block text-[10px]">YOUTUBE TITLE</span>
                  <span class="text-white font-bold block truncate mt-1">${meta.final_title || p.topic_title}</span>
                </button>
                <button onclick="copyToClipboard(\`${(meta.description || '').replace(/`/g, '\\`')}\`, 'Description')" class="p-3 bg-surface-900 hover:bg-surface-850 rounded-xl border border-surface-800 text-left">
                  <span class="text-zinc-500 block text-[10px]">DESCRIPTION & CHAPTERS</span>
                  <span class="text-crimson font-bold block mt-1">CLICK TO COPY FULL TEXT</span>
                </button>
                <button onclick="copyToClipboard('${(meta.tags || []).join(', ')}', 'SEO Tags')" class="p-3 bg-surface-900 hover:bg-surface-850 rounded-xl border border-surface-800 text-left">
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
      } else if (currentTab === "storyboard") {
        v.innerHTML = `
          <div class="space-y-6 max-w-6xl mx-auto">
            <div class="flex items-center justify-between">
              <div>
                <h2 class="text-xl font-black text-white uppercase tracking-wider font-mono">40-SCENE STORYBOARD</h2>
                <p class="text-xs text-zinc-400 font-mono mt-0.5">Click any scene card to open high-resolution Lightbox view.</p>
              </div>
              <span class="text-xs font-mono text-crimson font-bold">40 SCENES GENERATED</span>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3.5">
              ${scenes.map((s, idx) => {
                const scNum = (idx + 1).toString().padStart(2, "0");
                return `
                  <div onclick="openModal(${idx})" class="bg-surface-950 border border-surface-800 hover:border-crimson rounded-xl overflow-hidden cursor-pointer group transition-all">
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
      } else if (currentTab === "topics") {
        v.innerHTML = `
          <div class="space-y-6 max-w-5xl mx-auto">
            <div>
              <h2 class="text-xl font-black text-white uppercase tracking-wider font-mono">TOPIC RADAR (20 OPPORTUNITIES)</h2>
              <p class="text-xs text-zinc-400 font-mono mt-0.5">Ranked by audience curiosity and algorithm demand score.</p>
            </div>

            <div class="bg-surface-950 border border-surface-800 rounded-xl overflow-hidden">
              <table class="w-full text-left text-xs font-mono">
                <thead class="bg-surface-900 border-b border-surface-800 text-zinc-400">
                  <tr>
                    <th class="py-3 px-4">SCORE</th>
                    <th class="py-3 px-4">TOPIC CONCEPT</th>
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
                        <button onclick="buildTopic('${t.title.replace(/'/g, "\\'")}')" class="px-3 py-1 rounded bg-red-600 hover:bg-red-500 text-white font-bold text-xs glow-red transition">
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
      } else if (currentTab === "script") {
        v.innerHTML = `
          <div class="space-y-6 max-w-4xl mx-auto">
            <div class="flex items-center justify-between">
              <div>
                <h2 class="text-xl font-black text-white uppercase tracking-wider font-mono">5-ACT SCRIPT LEDGER</h2>
                <p class="text-xs text-zinc-400 font-mono mt-0.5">Full narrative text calibrated for 12.6-minute documentary delivery.</p>
              </div>
              <button onclick="copyToClipboard(document.getElementById('script-text').innerText, 'Script')" class="px-3 py-1.5 rounded bg-surface-850 hover:bg-surface-800 border border-surface-700 text-xs font-mono text-white">
                COPY SCRIPT
              </button>
            </div>

            <div class="bg-surface-950 border border-surface-800 rounded-xl p-6 space-y-6 font-mono" id="script-text">
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

    // High frequency progress poll (every 750ms) for real-time countdown & micro-meter
    setInterval(pollProgress, 750);

    // Full state poll every 3.5s
    setInterval(pollFull, 3500);

    // Initial startup
    pollProgress();
    pollFull();
  </script>
</body>
</html>
"""

for p_str in ["backend/app/templates/index.html", "backend/templates/index.html"]:
    p = Path(p_str)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(html_content, encoding="utf-8")
    print(f"Updated {p_str} with Live Mission Progress HUD & ETA Countdown.")
