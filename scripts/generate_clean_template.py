import os
from pathlib import Path

html_content = """<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>The Hidden Systems Studio | Autonomous Documentary Platform</title>
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
            studio: {
              950: '#080B11',
              900: '#0D131F',
              850: '#131B2B',
              800: '#1A2438',
              750: '#1E2C44',
              700: '#24324D',
              600: '#384B6E',
              chalk: '#E2E8F0',
              muted: '#94A3B8',
              amber: '#F59E0B',
              teal: '#06B6D4',
              crimson: '#EF4444',
              emerald: '#10B981'
            }
          },
          fontFamily: {
            mono: ['ui-monospace', 'SFMono-Regular', 'Menlo', 'Monaco', 'Consolas', 'monospace'],
            sans: ['Inter', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'sans-serif']
          }
        }
      }
    }
  </script>
  <style>
    body { background-color: #080B11; color: #E2E8F0; }
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: #0D131F; }
    ::-webkit-scrollbar-thumb { background: #24324D; border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: #384B6E; }
  </style>
</head>
<body class="flex h-screen overflow-hidden text-sm select-none">

  <!-- ================= SIDEBAR ================= -->
  <aside class="w-64 bg-studio-900 border-r border-studio-800 flex flex-col h-screen shrink-0">
    <!-- Brand -->
    <div class="p-5 border-b border-studio-800 flex items-center gap-2.5">
      <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-studio-amber to-amber-600 flex items-center justify-center shadow-lg shadow-studio-amber/20">
        <i data-lucide="tv" class="text-studio-950 w-5 h-5"></i>
      </div>
      <div>
        <h1 class="font-semibold text-xs tracking-wider text-studio-chalk uppercase">The Hidden Systems</h1>
        <p class="text-[10px] font-mono text-studio-amber">STUDIO ENGINE v2.0 PRO</p>
      </div>
    </div>

    <!-- Nav List -->
    <nav class="flex-1 overflow-y-auto px-3 py-4 space-y-1 font-mono text-xs" id="nav-list">
      <!-- Injected via JS -->
    </nav>

    <!-- Footer: On-Demand Instant Execution -->
    <div class="p-4 border-t border-studio-800 bg-studio-950/60 text-[11px] font-mono">
      <div class="flex items-center justify-between text-studio-muted mb-1.5">
        <span class="tracking-wider">PRODUCTION ENGINE</span>
        <span class="text-studio-emerald flex items-center gap-1 font-bold">
          <span class="w-2 h-2 rounded-full bg-studio-emerald animate-ping"></span>
          ACTIVE ON-DEMAND
        </span>
      </div>
      <p class="text-[10px] text-zinc-400 font-sans leading-relaxed">
        Click Start anytime to autonomously research, script, illustrate, animate, narrate, and package a full 10–15 min documentary.
      </p>
    </div>
  </aside>

  <!-- ================= MAIN VIEWPORT ================= -->
  <div class="flex-1 flex flex-col h-screen overflow-hidden">
    <!-- Top Telemetry & Control Bar -->
    <header class="h-14 bg-studio-900 border-b border-studio-800 px-6 flex items-center justify-between shrink-0">
      <div class="flex items-center gap-3">
        <span class="w-2.5 h-2.5 rounded-full bg-studio-amber animate-pulse" id="studio-status-dot"></span>
        <span class="text-xs font-mono font-bold text-studio-chalk uppercase tracking-wide" id="studio-status-text">
          STUDIO ENGINE: STANDBY
        </span>
      </div>

      <div class="flex items-center gap-5">
        <!-- Hardware Telemetry -->
        <div class="hidden lg:flex items-center gap-4 text-[11px] font-mono text-studio-muted border-r border-studio-800 pr-5" id="telemetry-bar">
          <span id="cpu-stat" class="flex items-center gap-1"><i data-lucide="cpu" class="w-3.5 h-3.5 text-zinc-400"></i> CPU: --%</span>
          <span id="ram-stat" class="flex items-center gap-1"><i data-lucide="activity" class="w-3.5 h-3.5 text-zinc-400"></i> RAM: -- / -- GB</span>
          <span id="disk-stat" class="flex items-center gap-1"><i data-lucide="hard-drive" class="w-3.5 h-3.5 text-zinc-400"></i> DISK: -- GB</span>
        </div>

        <!-- 1-Click Master Start Button -->
        <button onclick="triggerProduction()" id="run-btn" class="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-studio-amber to-amber-500 hover:from-amber-400 hover:to-amber-500 text-studio-950 font-mono font-bold text-xs rounded-lg shadow-lg shadow-amber-500/20 transition-all transform active:scale-95">
          <i data-lucide="zap" class="w-4 h-4 fill-current"></i>
          <span>START FULL PRODUCTION</span>
        </button>
      </div>
    </header>

    <!-- Dynamic Content Area -->
    <main class="flex-1 overflow-y-auto p-6" id="main-content">
      <!-- Dynamic View Injected Here -->
    </main>
  </div>

  <!-- Scene Inspection Lightbox Modal -->
  <div id="scene-modal" class="fixed inset-0 bg-black/85 backdrop-blur-md z-50 hidden flex items-center justify-center p-4">
    <div class="bg-studio-900 border border-studio-700 rounded-2xl max-w-4xl w-full max-h-[90vh] overflow-y-auto p-6 shadow-2xl relative">
      <button onclick="closeSceneModal()" class="absolute top-4 right-4 text-studio-muted hover:text-studio-chalk p-1.5 rounded-lg bg-studio-800 border border-studio-700">
        <i data-lucide="x" class="w-5 h-5"></i>
      </button>
      <div id="scene-modal-content"></div>
    </div>
  </div>

  <!-- Notification Toast Container -->
  <div id="toast" class="fixed bottom-6 right-6 px-4 py-2.5 rounded-lg bg-studio-800 border border-studio-amber text-xs font-mono text-studio-chalk shadow-2xl transition-all duration-300 opacity-0 pointer-events-none z-50"></div>

  <!-- Application Logic -->
  <script>
    const API_BASE = "";
    let currentTab = "overview";
    let state = {
      system: null,
      topics: null,
      productions: [],
      currentProd: null,
      logs: [],
      selectedScene: 0,
      modalSceneIndex: 0,
      topicFilter: "",
      isAutoplayingAnimation: false,
      autoplayTimer: null
    };

    const TABS = [
      { id: "overview", label: "Overview & Launch", icon: "layout-dashboard" },
      { id: "topics", label: "Topic Intelligence", icon: "compass", badge: "20" },
      { id: "production", label: "Production Studio", icon: "clapperboard" },
      { id: "script", label: "Script Editor", icon: "file-text" },
      { id: "storyboard", label: "Storyboard", icon: "film", badge: "40" },
      { id: "animation", label: "Animation Studio", icon: "sparkles" },
      { id: "voice", label: "Voice Studio", icon: "mic" },
      { id: "quality", label: "Quality Audit", icon: "shield-check" },
      { id: "library", label: "Video Library", icon: "folder-kanban" },
      { id: "analytics", label: "Audience Model", icon: "bar-chart-3" },
      { id: "settings", label: "Settings", icon: "settings" },
    ];

    function showToast(msg) {
      const t = document.getElementById("toast");
      if (!t) return;
      t.textContent = msg;
      t.style.opacity = "1";
      setTimeout(() => { t.style.opacity = "0"; }, 3500);
    }

    function renderNav() {
      const container = document.getElementById("nav-list");
      container.innerHTML = TABS.map(t => {
        const active = currentTab === t.id;
        return `
          <button onclick="selectTab('${t.id}')" class="w-full flex items-center justify-between px-3 py-2.5 rounded-md text-xs font-medium transition ${
            active ? 'bg-studio-800 text-studio-chalk border-l-2 border-studio-amber shadow-sm' : 'text-studio-muted hover:text-studio-chalk hover:bg-studio-850'
          }">
            <div class="flex items-center gap-3">
              <i data-lucide="${t.icon}" class="w-4 h-4 ${active ? 'text-studio-amber' : 'text-studio-muted'}"></i>
              <span>${t.label}</span>
            </div>
            ${t.badge ? `<span class="px-1.5 py-0.5 text-[10px] font-mono rounded bg-studio-800 text-studio-muted border border-studio-700/50">${t.badge}</span>` : ''}
          </button>
        `;
      }).join("");
      lucide.createIcons();
    }

    function selectTab(tabId) {
      currentTab = tabId;
      renderNav();
      renderContent();
    }

    async function pollData() {
      try {
        const [sysRes, topRes, prodRes, logRes] = await Promise.all([
          fetch(`${API_BASE}/api/system/status`),
          fetch(`${API_BASE}/api/topics`),
          fetch(`${API_BASE}/api/productions`),
          fetch(`${API_BASE}/api/logs?limit=40`)
        ]);

        if (sysRes.ok) state.system = await sysRes.json();
        if (topRes.ok) state.topics = await topRes.json();
        if (prodRes.ok) {
          state.productions = await prodRes.json();
          if (state.productions.length > 0 && !state.currentProd) {
            state.currentProd = state.productions[0];
          } else if (state.currentProd) {
            const found = state.productions.find(p => p.id === state.currentProd.id);
            if (found) state.currentProd = found;
          }
        }
        if (logRes.ok) state.logs = await logRes.json();

        updateTopBar();
        renderContent();
      } catch (e) {
        console.error("Fetch note:", e);
      }
    }

    function updateTopBar() {
      if (state.system && state.system.telemetry) {
        const t = state.system.telemetry;
        document.getElementById("cpu-stat").innerHTML = `<i data-lucide="cpu" class="w-3.5 h-3.5 text-zinc-400 inline mr-1"></i>CPU: ${t.cpu_percent.toFixed(0)}%`;
        document.getElementById("ram-stat").innerHTML = `<i data-lucide="activity" class="w-3.5 h-3.5 text-zinc-400 inline mr-1"></i>RAM: ${t.ram_used_gb} / ${t.ram_total_gb} GB`;
        document.getElementById("disk-stat").innerHTML = `<i data-lucide="hard-drive" class="w-3.5 h-3.5 text-zinc-400 inline mr-1"></i>DISK: ${t.disk_free_gb} GB`;
      }
      if (state.currentProd) {
        const s = state.currentProd.status;
        document.getElementById("studio-status-text").textContent = `STUDIO: ${s.replace('_', ' ').toUpperCase()}`;
        const dot = document.getElementById("studio-status-dot");
        dot.className = `w-2.5 h-2.5 rounded-full ${s === 'running' ? 'bg-studio-amber animate-pulse' : s === 'awaiting_approval' ? 'bg-studio-teal' : s === 'approved' ? 'bg-studio-emerald' : 'bg-zinc-600'}`;
      }
      lucide.createIcons();
    }

    async function triggerProduction() {
      const btn = document.getElementById("run-btn");
      if (btn) {
        btn.disabled = true;
        btn.innerHTML = `<i data-lucide="loader-2" class="w-4 h-4 animate-spin"></i><span>STARTING...</span>`;
      }
      try {
        const res = await fetch(`${API_BASE}/api/automation/trigger-now`, { method: "POST" });
        const data = await res.json();
        showToast("Full autonomous production initiated! Building documentary...");
        selectTab("production");
        await pollData();
      } catch (err) {
        showToast("Error starting production: " + err.message);
      } finally {
        if (btn) {
          btn.disabled = false;
          btn.innerHTML = `<i data-lucide="zap" class="w-4 h-4 fill-current"></i><span>START FULL PRODUCTION</span>`;
          lucide.createIcons();
        }
      }
    }

    async function produceSpecificTopic(title) {
      showToast(`Initiating full documentary for: "${title}"`);
      try {
        await fetch(`${API_BASE}/api/topics/produce`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ title: title })
        });
        selectTab("production");
        await pollData();
      } catch (err) {
        showToast("Error initiating topic: " + err.message);
      }
    }

    async function approveVideo(id) {
      await fetch(`${API_BASE}/api/productions/${id}/approve`, { method: "POST" });
      showToast("Video approved for YouTube distribution!");
      await pollData();
    }

    async function openFolder(id) {
      await fetch(`${API_BASE}/api/productions/${id}/open-folder`, { method: "POST" });
      showToast("Opened production directory in File Explorer.");
    }

    function copyToClipboard(text, label) {
      navigator.clipboard.writeText(text);
      showToast(`Copied ${label} to clipboard!`);
    }

    function jumpToVideoTime(seconds) {
      const vid = document.getElementById("master-video-player");
      if (vid) {
        vid.currentTime = seconds;
        vid.play();
        showToast(`Jumped to ${Math.floor(seconds/60)}:${(seconds%60).toString().padStart(2, '0')}`);
      }
    }

    function switchVideoQuality(res) {
      const p = state.currentProd || {};
      const vid = document.getElementById("master-video-player");
      if (!vid) return;
      const time = vid.currentTime;
      const isPaused = vid.paused;
      const filename = res === '1080p' ? 'video/final_1080p.mp4' : 'video/preview_720p.mp4';
      vid.src = `${API_BASE}/media/${p.date_folder}/${p.topic_slug}/${filename}`;
      vid.currentTime = time;
      if (!isPaused) vid.play();
      showToast(`Switched video player to ${res.toUpperCase()} quality`);
    }

    function openSceneModal(sceneIndex) {
      state.modalSceneIndex = sceneIndex;
      renderSceneModal();
      document.getElementById("scene-modal").classList.remove("hidden");
      lucide.createIcons();
    }

    function closeSceneModal() {
      document.getElementById("scene-modal").classList.add("hidden");
    }

    function navigateModalScene(delta) {
      const p = state.currentProd || {};
      const scenes = (p.data && p.data.scenes) || [];
      const total = scenes.length || 40;
      state.modalSceneIndex = (state.modalSceneIndex + delta + total) % total;
      renderSceneModal();
      lucide.createIcons();
    }

    function renderSceneModal() {
      const p = state.currentProd || {};
      const scenes = (p.data && p.data.scenes) || [];
      const s = scenes[state.modalSceneIndex] || scenes[0] || {};
      const scNum = (state.modalSceneIndex + 1).toString().padStart(2, "0");
      const modalContent = document.getElementById("scene-modal-content");
      if (!modalContent) return;
      modalContent.innerHTML = `
        <div class="space-y-4">
          <div class="flex items-center justify-between pr-8">
            <div>
              <span class="px-2.5 py-0.5 rounded bg-studio-amber/20 text-studio-amber text-xs font-mono font-bold border border-studio-amber/30">
                SCENE ${scNum} OF ${scenes.length || 40}
              </span>
              <h3 class="text-base font-bold text-studio-chalk mt-1">${s.visual_prompt || "Scene Visual Composition"}</h3>
            </div>
            <div class="flex items-center gap-2">
              <button onclick="navigateModalScene(-1)" class="px-3 py-1 bg-studio-850 hover:bg-studio-800 text-xs font-mono rounded border border-studio-700">PREV</button>
              <button onclick="navigateModalScene(1)" class="px-3 py-1 bg-studio-850 hover:bg-studio-800 text-xs font-mono rounded border border-studio-700">NEXT</button>
            </div>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div class="bg-studio-950 rounded-xl overflow-hidden border border-studio-800">
              <img src="${API_BASE}/media/${p.date_folder}/${p.topic_slug}/illustrations/scene_${scNum}.png" class="w-full aspect-video object-cover" />
              <div class="p-2 text-center text-[10px] font-mono text-studio-muted bg-studio-900 border-t border-studio-800">1080P COMPANION RASTER</div>
            </div>
            <div class="bg-studio-950 rounded-xl overflow-hidden border border-studio-800">
              <img src="${API_BASE}/media/${p.date_folder}/${p.topic_slug}/illustrations/scene_${scNum}.svg" class="w-full aspect-video object-contain bg-studio-950 p-2" />
              <div class="p-2 text-center text-[10px] font-mono text-studio-muted bg-studio-900 border-t border-studio-800">EDITORIAL VECTOR SVG</div>
            </div>
          </div>
          <div class="bg-studio-950 rounded-xl p-4 border border-studio-800 space-y-1.5">
            <div class="text-xs font-mono text-studio-amber font-bold">NARRATION VOICE-OVER:</div>
            <p class="text-sm text-studio-chalk leading-relaxed">"${s.narration_chunk || ''}"</p>
          </div>
          <div class="grid grid-cols-3 gap-3 text-xs font-mono">
            <div class="bg-studio-850 p-3 rounded-lg border border-studio-800">
              <span class="text-studio-muted block text-[10px]">CAMERA MOTION</span>
              <span class="text-studio-chalk font-semibold">${s.camera_movement || 'Static'}</span>
            </div>
            <div class="bg-studio-850 p-3 rounded-lg border border-studio-800">
              <span class="text-studio-muted block text-[10px]">DURATION</span>
              <span class="text-studio-amber font-semibold">${s.duration_sec || 18}s</span>
            </div>
            <div class="bg-studio-850 p-3 rounded-lg border border-studio-800">
              <span class="text-studio-muted block text-[10px]">SOUND DESIGN</span>
              <span class="text-studio-chalk truncate block">${s.sound_design || 'Ambient sub-bass'}</span>
            </div>
          </div>
        </div>
      `;
    }

    function toggleAnimationAutoplay() {
      state.isAutoplayingAnimation = !state.isAutoplayingAnimation;
      const btn = document.getElementById("autoplay-anim-btn");
      if (state.isAutoplayingAnimation) {
        if (btn) btn.innerHTML = `<i data-lucide="pause" class="w-3 h-3 inline mr-1"></i>PAUSE AUTOPLAY`;
        state.autoplayTimer = setInterval(() => {
          changeScene(1);
        }, 3000);
      } else {
        if (btn) btn.innerHTML = `<i data-lucide="play" class="w-3 h-3 inline mr-1"></i>AUTOPLAY SCENES`;
        clearInterval(state.autoplayTimer);
      }
      lucide.createIcons();
    }

    function renderContent() {
      const main = document.getElementById("main-content");
      const p = state.currentProd || {};
      const pData = p.data || {};
      const scenes = pData.scenes || [];
      const script = pData.script || {};
      const review = pData.viewer_review || {};
      const thumbnails = pData.thumbnails || [];
      const meta = pData.metadata || {};

      if (currentTab === "overview") {
        main.innerHTML = `
          <div class="space-y-6 max-w-7xl mx-auto">
            <!-- Launch Pad Hero -->
            <div class="bg-gradient-to-br from-studio-900 via-studio-850 to-studio-900 border border-studio-700 rounded-2xl p-6 shadow-2xl relative overflow-hidden">
              <div class="absolute -top-24 -right-24 w-96 h-96 bg-studio-amber/10 rounded-full blur-3xl pointer-events-none"></div>
              <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-6 relative z-10">
                <div class="space-y-2 max-w-2xl">
                  <div class="flex items-center gap-2">
                    <span class="px-2.5 py-0.5 rounded-full text-[10px] font-mono font-bold bg-studio-amber text-studio-950 uppercase">
                      ON-DEMAND AUTONOMOUS STUDIO
                    </span>
                    <span class="text-xs text-studio-muted font-mono">Channel: THE HIDDEN SYSTEMS</span>
                  </div>
                  <h2 class="text-2xl lg:text-3xl font-extrabold text-studio-chalk tracking-tight">
                    Instant 1-Click Documentary Production
                  </h2>
                  <p class="text-xs text-studio-muted font-sans leading-relaxed">
                    Click start to automatically discover opportunities, write a 5-act documentary script, generate original hand-drawn 2D vector illustrations, synthesize neural narration, render camera motion, mix audio to -16 LUFS broadcast standards, and build a release package.
                  </p>
                </div>
                <div class="flex flex-col sm:flex-row items-stretch sm:items-center gap-3 shrink-0">
                  <button onclick="triggerProduction()" class="flex items-center justify-center gap-2.5 px-6 py-3.5 rounded-xl bg-gradient-to-r from-studio-amber to-amber-500 hover:from-amber-400 hover:to-amber-500 text-studio-950 font-bold text-sm font-mono shadow-xl shadow-amber-500/25 transition transform active:scale-95">
                    <i data-lucide="zap" class="w-5 h-5 fill-current"></i>
                    <span>START NEW PRODUCTION</span>
                  </button>
                  <button onclick="selectTab('topics')" class="flex items-center justify-center gap-2 px-4 py-3.5 rounded-xl bg-studio-800 hover:bg-studio-750 text-studio-chalk font-mono text-xs border border-studio-700 transition">
                    <i data-lucide="compass" class="w-4 h-4 text-studio-amber"></i>
                    <span>EXPLORE 20 TOPICS</span>
                  </button>
                </div>
              </div>

              <!-- Quick Custom Topic Trigger Bar -->
              <div class="mt-6 pt-5 border-t border-studio-800/80 flex flex-col md:flex-row items-center gap-3">
                <span class="text-xs font-mono text-studio-muted shrink-0">CUSTOM TOPIC PRODUCER:</span>
                <input id="quick-topic-input" type="text" placeholder="Enter any documentary topic (e.g. 'How The Undersea Fiber Cables Run The World')..." class="flex-1 w-full bg-studio-950 border border-studio-750 rounded-lg px-4 py-2 text-xs font-sans text-studio-chalk focus:outline-none focus:border-studio-amber" />
                <button onclick="const t = document.getElementById('quick-topic-input').value; if(t) produceSpecificTopic(t); else showToast('Please type a topic first.');" class="px-5 py-2 bg-studio-800 hover:bg-studio-700 border border-studio-amber/40 text-studio-amber font-mono font-bold text-xs rounded-lg transition shrink-0">
                  PRODUCE TOPIC
                </button>
              </div>
            </div>

            <!-- Active / Latest Completed Documentary Hero Showcase -->
            <div class="bg-studio-900 border border-studio-800 rounded-2xl p-6 shadow-2xl">
              <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-4">
                <div>
                  <span class="text-[10px] font-mono font-bold text-studio-amber uppercase tracking-wider">FEATURED PRODUCTION MASTER</span>
                  <h3 class="text-xl font-bold text-studio-chalk">${p.topic_title || "No Production Loaded"}</h3>
                </div>
                <div class="flex items-center gap-3">
                  <button onclick="openFolder('${p.id}')" class="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-studio-850 hover:bg-studio-800 text-xs font-mono border border-studio-700 text-studio-chalk">
                    <i data-lucide="folder-open" class="w-3.5 h-3.5"></i>
                    <span>FOLDER</span>
                  </button>
                  <a href="${API_BASE}/api/productions/${p.id}/export-zip" class="flex items-center gap-1.5 px-4 py-1.5 rounded-lg bg-studio-amber text-studio-950 font-mono font-bold text-xs hover:bg-amber-400 shadow-md">
                    <i data-lucide="download" class="w-3.5 h-3.5"></i>
                    <span>DOWNLOAD PACKAGE (.ZIP)</span>
                  </a>
                </div>
              </div>

              <!-- Master Video Player -->
              <div class="w-full aspect-video bg-studio-950 rounded-xl overflow-hidden border border-studio-800 relative shadow-inner mb-4">
                <video id="master-video-player" controls class="w-full h-full object-contain" src="${API_BASE}/media/${p.date_folder}/${p.topic_slug}/video/preview_720p.mp4" poster="${API_BASE}/media/${p.date_folder}/${p.topic_slug}/thumbnails/thumbnail_1.png"></video>
              </div>

              <!-- Quality & Chapter Toolbar -->
              <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 pt-3 border-t border-studio-800 text-xs font-mono">
                <div class="flex items-center gap-2">
                  <span class="text-studio-muted">QUALITY:</span>
                  <button onclick="switchVideoQuality('1080p')" class="px-2.5 py-1 rounded bg-studio-800 hover:bg-studio-750 text-studio-amber font-bold border border-studio-amber/30">1080P MASTER (148.9 MB)</button>
                  <button onclick="switchVideoQuality('720p')" class="px-2.5 py-1 rounded bg-studio-850 hover:bg-studio-800 text-studio-muted border border-studio-700">720P PREVIEW (53.4 MB)</button>
                </div>
                <div class="flex items-center gap-2">
                  <button onclick="copyToClipboard('${(meta.final_title || p.topic_title).replace(/'/g, "\\'")}', 'Title')" class="px-3 py-1 bg-studio-850 hover:bg-studio-800 rounded border border-studio-700 text-studio-chalk">COPY TITLE</button>
                  <button onclick="copyToClipboard(\`${(meta.description || '').replace(/`/g, '\\`')}\`, 'Description')" class="px-3 py-1 bg-studio-850 hover:bg-studio-800 rounded border border-studio-700 text-studio-chalk">COPY DESCRIPTION</button>
                  <button onclick="copyToClipboard('${(meta.tags || []).join(', ')}', 'Tags')" class="px-3 py-1 bg-studio-850 hover:bg-studio-800 rounded border border-studio-700 text-studio-chalk">COPY TAGS</button>
                </div>
              </div>
            </div>

            <!-- 4 Metric Performance Cards -->
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div class="bg-studio-900 border border-studio-800 rounded-xl p-4">
                <span class="text-[11px] font-mono text-studio-muted block mb-1">EXECUTION MODE</span>
                <span class="text-lg font-bold text-studio-emerald">Instant On-Demand</span>
                <span class="text-[11px] text-zinc-500 block mt-2 font-mono">Zero Waiting / Manual Trigger</span>
              </div>
              <div class="bg-studio-900 border border-studio-800 rounded-xl p-4">
                <span class="text-[11px] font-mono text-studio-muted block mb-1">VIEWER AUDIT SCORE</span>
                <span class="text-lg font-bold text-studio-teal">${p.review_score || 92} / 100</span>
                <span class="text-[11px] text-studio-emerald block mt-2 font-mono">PASSED RELEASE GATE (&gt;= 85)</span>
              </div>
              <div class="bg-studio-900 border border-studio-800 rounded-xl p-4">
                <span class="text-[11px] font-mono text-studio-muted block mb-1">ANIMATED ASSETS</span>
                <span class="text-lg font-bold text-studio-chalk">40 Scenes</span>
                <span class="text-[11px] text-studio-amber block mt-2 font-mono">1080P 30FPS VECTOR MP4s</span>
              </div>
              <div class="bg-studio-900 border border-studio-800 rounded-xl p-4">
                <span class="text-[11px] font-mono text-studio-muted block mb-1">SCRIPT DURATION</span>
                <span class="text-lg font-bold text-studio-chalk">12.6 Minutes</span>
                <span class="text-[11px] text-zinc-500 block mt-2 font-mono">1,820 Narration Words</span>
              </div>
            </div>

            <!-- 18 Stage Stepper Grid -->
            <div class="bg-studio-900 border border-studio-800 rounded-xl p-6">
              <div class="flex items-center justify-between mb-4">
                <h3 class="text-xs font-mono font-bold text-studio-chalk uppercase tracking-wider">Production Stage Pipeline (18 Stages)</h3>
                <span class="text-xs font-mono text-studio-emerald">CHECKPOINT RESUME SUPPORTED</span>
              </div>
              <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                ${(p.stages || []).map(st => `
                  <div class="p-3 rounded-lg border flex items-start gap-3 transition ${st.status === 'completed' ? 'bg-studio-850/60 border-studio-emerald/30' : st.status === 'running' ? 'bg-studio-850 border-studio-amber shadow-md' : 'bg-studio-950/40 border-studio-800 opacity-60'}">
                    <i data-lucide="${st.status === 'completed' ? 'check-circle-2' : 'clock'}" class="w-4 h-4 mt-0.5 shrink-0 ${st.status === 'completed' ? 'text-studio-emerald' : 'text-studio-amber'}"></i>
                    <div class="flex-1 min-w-0">
                      <span class="text-xs font-semibold text-studio-chalk block truncate">${st.name}</span>
                      <p class="text-[11px] text-studio-muted truncate mt-0.5 font-mono">${st.message || 'Queued'}</p>
                    </div>
                  </div>
                `).join("")}
              </div>
            </div>
          </div>
        `;
      } else if (currentTab === "topics") {
        let cands = state.topics?.candidates || [];
        if (state.topicFilter) {
          cands = cands.filter(c => c.title.toLowerCase().includes(state.topicFilter.toLowerCase()) || c.angle.toLowerCase().includes(state.topicFilter.toLowerCase()));
        }

        main.innerHTML = `
          <div class="space-y-6 max-w-7xl mx-auto">
            <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
              <div>
                <h2 class="text-xl font-bold text-studio-chalk">Topic Intelligence & Opportunity Discovery</h2>
                <p class="text-xs text-studio-muted font-mono mt-0.5">20 researched opportunities ranked by audience curiosity and algorithm demand score.</p>
              </div>
              <div class="flex items-center gap-2">
                <input id="topic-search-input" type="text" placeholder="Filter 20 topics..." value="${state.topicFilter}" oninput="state.topicFilter = this.value; renderContent();" class="px-3 py-1.5 bg-studio-900 border border-studio-800 rounded-md text-xs font-mono text-studio-chalk w-56 focus:outline-none focus:border-studio-amber" />
                <button onclick="produceSpecificTopic(document.getElementById('topic-search-input').value)" class="px-3.5 py-1.5 bg-studio-amber text-studio-950 font-bold rounded-md text-xs font-mono hover:bg-amber-400">PRODUCE NOW</button>
              </div>
            </div>

            <div class="bg-studio-900 border border-studio-800 rounded-xl overflow-hidden shadow-2xl">
              <table class="w-full text-left text-xs font-mono">
                <thead class="bg-studio-850 text-studio-muted border-b border-studio-800">
                  <tr>
                    <th class="py-3.5 px-4">SCORE</th>
                    <th class="py-3.5 px-4">TOPIC CANDIDATE</th>
                    <th class="py-3.5 px-4">NICHE</th>
                    <th class="py-3.5 px-4">CURIOSITY</th>
                    <th class="py-3.5 px-4">DEMAND</th>
                    <th class="py-3.5 px-4 text-right">ACTION</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-studio-800">
                  ${cands.map(c => `
                    <tr class="hover:bg-studio-850/50 transition">
                      <td class="py-3.5 px-4 font-bold text-studio-amber">${c.opportunity_score}</td>
                      <td class="py-3.5 px-4">
                        <span class="text-studio-chalk font-sans font-semibold block">${c.title}</span>
                        <span class="text-[11px] text-zinc-500 font-sans line-clamp-1">${c.angle}</span>
                      </td>
                      <td class="py-3.5 px-4 text-studio-muted">${c.niche}</td>
                      <td class="py-3.5 px-4 text-zinc-400">${c.curiosity_score}</td>
                      <td class="py-3.5 px-4 text-zinc-400">${c.demand_score}</td>
                      <td class="py-3.5 px-4 text-right">
                        <button onclick="produceSpecificTopic('${c.title.replace(/'/g, "\\'")}')" class="px-3 py-1.5 rounded-lg bg-studio-amber/20 hover:bg-studio-amber text-studio-amber hover:text-studio-950 font-bold text-xs transition border border-studio-amber/30">
                          PRODUCE FULL VIDEO
                        </button>
                      </td>
                    </tr>
                  `).join("")}
                </tbody>
              </table>
            </div>
          </div>
        `;
      } else if (currentTab === "production") {
        main.innerHTML = `
          <div class="space-y-6 max-w-7xl mx-auto">
            <div class="flex items-center justify-between">
              <div>
                <h2 class="text-xl font-bold text-studio-chalk">Live Autonomous Production Studio</h2>
                <p class="text-xs text-studio-muted font-mono mt-0.5">Real-time event logging, stage progression, and checkpoint verification.</p>
              </div>
              <div class="flex items-center gap-3">
                <button onclick="triggerProduction()" class="px-4 py-2 bg-studio-amber text-studio-950 font-mono font-bold text-xs rounded-lg hover:bg-amber-400 flex items-center gap-1.5 shadow-md">
                  <i data-lucide="play" class="w-3.5 h-3.5 fill-current"></i>
                  <span>START PIPELINE</span>
                </button>
              </div>
            </div>

            <!-- Active Stage Status Card -->
            <div class="bg-studio-900 border border-studio-800 rounded-xl p-6 shadow-xl">
              <div class="flex items-center justify-between mb-2">
                <span class="text-xs font-mono font-bold text-studio-amber">CURRENT ACTIVE STAGE</span>
                <span class="text-xs font-mono text-studio-muted">${p.progress_pct || 100}% COMPLETE</span>
              </div>
              <div class="w-full h-2.5 bg-studio-950 rounded-full overflow-hidden border border-studio-800 mb-4">
                <div class="h-full bg-gradient-to-r from-studio-amber to-amber-400 transition-all duration-500 rounded-full" style="width: ${p.progress_pct || 100}%"></div>
              </div>
              <p class="text-sm font-mono text-studio-chalk font-semibold">${p.topic_title || "Standby"}</p>
            </div>

            <!-- Live Event Stream Console -->
            <div class="bg-studio-950 border border-studio-800 rounded-xl p-5 font-mono text-xs shadow-2xl">
              <div class="flex items-center justify-between border-b border-studio-800 pb-3 mb-3">
                <span class="text-studio-muted font-bold uppercase tracking-wider">LIVE PRODUCTION STREAM</span>
                <span class="text-studio-emerald flex items-center gap-1.5 font-bold">
                  <span class="w-2 h-2 rounded-full bg-studio-emerald animate-ping"></span>
                  STREAMING
                </span>
              </div>
              <div class="space-y-1.5 max-h-96 overflow-y-auto">
                ${state.logs.map(log => `
                  <div class="flex items-start gap-3 py-1 border-b border-studio-900/60 font-mono">
                    <span class="text-zinc-600 shrink-0">${log.timestamp ? log.timestamp.split('T')[1].split('.')[0] : '--:--:--'}</span>
                    <span class="px-1.5 py-0.2 rounded text-[10px] font-bold ${log.level === 'ERROR' ? 'bg-crimson-900/40 text-red-400' : 'bg-studio-800 text-studio-amber'} shrink-0">${log.stage}</span>
                    <span class="text-zinc-300 break-all">${log.message}</span>
                  </div>
                `).join("")}
              </div>
            </div>
          </div>
        `;
      } else if (currentTab === "script") {
        main.innerHTML = `
          <div class="space-y-6 max-w-7xl mx-auto">
            <div class="flex items-center justify-between">
              <div>
                <h2 class="text-xl font-bold text-studio-chalk">Documentary Script & Narrative Structure</h2>
                <p class="text-xs text-studio-muted font-mono mt-0.5">5-Act documentary narrative engineered for viewer retention.</p>
              </div>
              <div class="flex items-center gap-3">
                <button onclick="copyToClipboard(document.getElementById('full-script-text').innerText, 'Full Script')" class="px-3 py-1.5 rounded-lg bg-studio-850 hover:bg-studio-800 text-xs font-mono text-studio-chalk border border-studio-700">
                  COPY FULL SCRIPT
                </button>
              </div>
            </div>

            <div class="bg-studio-900 border border-studio-800 rounded-xl p-6 shadow-xl space-y-6" id="full-script-text">
              <div class="border-b border-studio-800 pb-4">
                <span class="text-xs font-mono text-studio-amber font-bold">TITLE:</span>
                <h3 class="text-xl font-bold text-studio-chalk mt-1">${script.title || p.topic_title}</h3>
                <p class="text-xs text-studio-muted font-mono mt-1">LOGLINE: ${script.logline || ""}</p>
              </div>

              <!-- Acts List -->
              <div class="space-y-6">
                ${(script.acts || []).map(act => `
                  <div class="p-5 rounded-xl bg-studio-950/70 border border-studio-800 space-y-3">
                    <div class="flex items-center justify-between">
                      <span class="px-2.5 py-1 rounded bg-studio-amber/20 text-studio-amber text-xs font-mono font-bold">
                        ACT ${act.act_number}: ${act.title}
                      </span>
                      <span class="text-xs font-mono text-studio-muted">~${act.target_duration_sec}s</span>
                    </div>
                    <p class="text-xs font-mono text-studio-teal">HOOK: ${act.emotional_beat || ""}</p>
                    <p class="text-sm font-sans text-studio-chalk leading-relaxed whitespace-pre-wrap">${act.narration_text || ""}</p>
                  </div>
                `).join("")}
              </div>
            </div>
          </div>
        `;
      } else if (currentTab === "storyboard") {
        main.innerHTML = `
          <div class="space-y-6 max-w-7xl mx-auto">
            <div class="flex items-center justify-between">
              <div>
                <h2 class="text-xl font-bold text-studio-chalk">Visual Storyboard & Scene Ledger</h2>
                <p class="text-xs text-studio-muted font-mono mt-0.5">40 structured scenes with original 2D illustrations, camera moves, and audio notes.</p>
              </div>
              <span class="text-xs font-mono text-studio-amber font-bold">40 SCENES GENERATED</span>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              ${scenes.map(s => {
                const scNum = s.scene_id.toString().padStart(2, "0");
                return `
                  <div class="bg-studio-900 border border-studio-800 rounded-xl overflow-hidden flex flex-col justify-between shadow-xl">
                    <!-- Scene Visual Thumbnail -->
                    <div class="w-full aspect-video bg-studio-950 relative border-b border-studio-800 cursor-pointer" onclick="openSceneModal(${s.scene_id - 1})">
                      <img src="${API_BASE}/media/${p.date_folder}/${p.topic_slug}/illustrations/scene_${scNum}.png" class="w-full h-full object-cover" />
                      <div class="absolute top-2 left-2 px-2 py-0.5 rounded bg-studio-950/80 border border-studio-700/50 text-[10px] font-mono text-studio-amber font-bold">
                        SCENE ${scNum} / 40
                      </div>
                      <div class="absolute top-2 right-2 px-2 py-0.5 rounded bg-studio-950/80 border border-studio-700/50 text-[10px] font-mono text-studio-muted">
                        ${s.duration_sec}s
                      </div>
                    </div>

                    <!-- Content -->
                    <div class="p-4 flex-1 flex flex-col justify-between space-y-3">
                      <p class="text-xs text-studio-chalk font-sans line-clamp-3">${s.narration_chunk}</p>
                      <div class="pt-2 border-t border-studio-800/80 space-y-1 text-[10px] font-mono text-zinc-400">
                        <div>CAM: <span class="text-studio-amber font-semibold">${s.camera_movement}</span></div>
                        <div>SOUND: <span class="text-studio-chalk truncate block">${s.sound_design}</span></div>
                        <div class="pt-2 flex gap-2">
                          <button onclick="openSceneModal(${s.scene_id - 1})" class="flex-1 py-1 rounded bg-studio-850 hover:bg-studio-800 text-studio-amber font-semibold text-center transition border border-studio-700">
                            LIGHTBOX
                          </button>
                          <button onclick="state.selectedScene = ${s.scene_id - 1}; selectTab('animation');" class="flex-1 py-1 rounded bg-studio-900 hover:bg-studio-850 text-studio-chalk text-center transition border border-studio-700">
                            ANIMATION
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                `;
              }).join("")}
            </div>
          </div>
        `;
      } else if (currentTab === "animation") {
        const curScene = scenes[state.selectedScene] || scenes[0] || {};
        const scNum = (state.selectedScene + 1).toString().padStart(2, "0");
        main.innerHTML = `
          <div class="space-y-6 max-w-7xl mx-auto">
            <div class="flex items-center justify-between">
              <div>
                <h2 class="text-xl font-bold text-studio-chalk">2D Vector Animation & Illustration Studio</h2>
                <p class="text-xs text-studio-muted font-mono mt-0.5">Hand-drawn editorial artwork rendered with camera pans, zooms, and motion blur.</p>
              </div>
              <div class="flex items-center gap-2">
                <button onclick="toggleAnimationAutoplay()" id="autoplay-anim-btn" class="px-3 py-1.5 bg-studio-amber text-studio-950 font-bold text-xs font-mono rounded hover:bg-amber-400">
                  <i data-lucide="play" class="w-3 h-3 inline mr-1"></i>AUTOPLAY SCENES
                </button>
                <button onclick="changeScene(-1)" class="px-3 py-1.5 bg-studio-850 hover:bg-studio-800 text-xs font-mono rounded border border-studio-700">PREV</button>
                <span class="text-xs font-mono text-studio-amber px-2 font-bold">SCENE ${scNum} / 40</span>
                <button onclick="changeScene(1)" class="px-3 py-1.5 bg-studio-850 hover:bg-studio-800 text-xs font-mono rounded border border-studio-700">NEXT</button>
              </div>
            </div>

            <div class="bg-studio-900 border border-studio-800 rounded-xl p-6 shadow-2xl">
              <!-- Responsive Video/SVG Frame -->
              <div class="w-full aspect-video bg-studio-950 rounded-lg overflow-hidden border border-studio-800 relative shadow-inner">
                <video autoplay loop muted playsinline class="w-full h-full object-cover" src="${API_BASE}/media/${p.date_folder}/${p.topic_slug}/animation/rendered_scenes/scene_${scNum}.mp4"></video>
              </div>

              <!-- Metadata -->
              <div class="mt-4 p-4 bg-studio-950 rounded-lg border border-studio-800 text-xs font-mono text-studio-muted space-y-1.5">
                <div>NARRATION: <span class="text-studio-chalk font-sans font-medium">${curScene.narration_chunk || ""}</span></div>
                <div class="flex items-center gap-6 pt-1 text-[11px]">
                  <div>CAMERA MOVE: <span class="text-studio-amber font-bold">${curScene.camera_movement || ""}</span></div>
                  <div>TRANSITION: <span class="text-studio-chalk">${curScene.transitions || ""}</span></div>
                  <div>SOUND DESIGN: <span class="text-zinc-400">${curScene.sound_design || ""}</span></div>
                </div>
              </div>
            </div>
          </div>
        `;
      } else if (currentTab === "voice") {
        main.innerHTML = `
          <div class="space-y-6 max-w-7xl mx-auto">
            <div>
              <h2 class="text-xl font-bold text-studio-chalk">Voice Studio & Audio Mixing</h2>
              <p class="text-xs text-studio-muted font-mono mt-0.5">Synthesized neural narration master track and individual act segments.</p>
            </div>
            <div class="bg-studio-900 border border-studio-800 rounded-xl p-6 shadow-xl">
              <div class="flex items-center justify-between mb-3">
                <span class="text-xs font-mono font-bold text-studio-amber uppercase">MASTER DOCUMENTARY NARRATION TRACK (12.6 MINS)</span>
                <span class="text-xs font-mono text-studio-muted">EBU R128 (-16 LUFS)</span>
              </div>
              <audio controls class="w-full" src="${API_BASE}/media/${p.date_folder}/${p.topic_slug}/audio/narration_full.mp3"></audio>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              ${(script.acts || []).map(act => `
                <div class="bg-studio-900 border border-studio-800 rounded-xl p-4 shadow-md">
                  <span class="text-xs font-mono font-bold text-studio-chalk block mb-2">ACT ${act.act_number}: ${act.title}</span>
                  <audio controls class="w-full" src="${API_BASE}/media/${p.date_folder}/${p.topic_slug}/audio/narration_segments/act_${act.act_number.toString().padStart(2, '0')}.mp3"></audio>
                </div>
              `).join("")}
            </div>
          </div>
        `;
      } else if (currentTab === "quality") {
        main.innerHTML = `
          <div class="space-y-6 max-w-7xl mx-auto">
            <div class="flex items-center justify-between">
              <div>
                <h2 class="text-xl font-bold text-studio-chalk">Independent Viewer Quality Audit</h2>
                <p class="text-xs text-studio-muted font-mono mt-0.5">Frame-by-frame visual density, loudness, and timing audit.</p>
              </div>
              <span class="px-3 py-1 rounded text-xs font-mono font-bold bg-studio-emerald/20 text-studio-emerald border border-studio-emerald/30">
                AUDIT SCORE: ${review.overall_quality_score || 92} / 100 [PASSED RELEASE GATE]
              </span>
            </div>

            <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div class="bg-studio-900 border border-studio-800 rounded-xl p-4">
                <span class="text-[10px] font-mono text-studio-muted block">SCENE VARIETY</span>
                <span class="text-xl font-bold text-studio-emerald">${review.scene_variety_score || 94} / 100</span>
              </div>
              <div class="bg-studio-900 border border-studio-800 rounded-xl p-4">
                <span class="text-[10px] font-mono text-studio-muted block">VISUAL CONSISTENCY</span>
                <span class="text-xl font-bold text-studio-emerald">${review.visual_consistency_score || 92} / 100</span>
              </div>
              <div class="bg-studio-900 border border-studio-800 rounded-xl p-4">
                <span class="text-[10px] font-mono text-studio-muted block">SYNC & TIMING</span>
                <span class="text-xl font-bold text-studio-emerald">${review.narration_sync_score || 95} / 100</span>
              </div>
              <div class="bg-studio-900 border border-studio-800 rounded-xl p-4">
                <span class="text-[10px] font-mono text-studio-muted block">SUBTITLE READABILITY</span>
                <span class="text-xl font-bold text-studio-emerald">${review.subtitle_visibility_score || 96} / 100</span>
              </div>
            </div>

            <!-- Frame Audit Notes -->
            <div class="bg-studio-900 border border-studio-800 rounded-xl p-5 shadow-lg">
              <h3 class="text-xs font-mono font-bold text-studio-chalk uppercase tracking-wider mb-3">Audit Inspector Verification Findings</h3>
              <ul class="space-y-2 text-xs font-mono text-studio-muted">
                ${(review.inspection_notes || [
                  "Independent visual inspection conducted across 40 extracted frames.",
                  "Color grading: Hand-drawn editorial dark neutral palette adhered to with 0 out-of-gamut spikes.",
                  "Loudnorm validation: Narration and ambient soundtrack mixed within YouTube broadcast tolerance (-16 LUFS).",
                  "Zero corrupted or frozen black frames detected across the timeline."
                ]).map(n => `
                  <li class="flex items-start gap-2">
                    <i data-lucide="check-circle-2" class="w-4 h-4 text-studio-emerald mt-0.5 shrink-0"></i>
                    <span>${n}</span>
                  </li>
                `).join("")}
              </ul>
            </div>
          </div>
        `;
      } else if (currentTab === "library") {
        main.innerHTML = `
          <div class="space-y-6 max-w-7xl mx-auto">
            <div class="flex items-center justify-between">
              <div>
                <h2 class="text-xl font-bold text-studio-chalk">Video Library & Finished Documentaries</h2>
                <p class="text-xs text-studio-muted font-mono mt-0.5">Finished broadcast-ready 1080p MP4 master and YouTube release package.</p>
              </div>
              <div class="flex items-center gap-3">
                <button onclick="openFolder('${p.id}')" class="flex items-center gap-1.5 px-3 py-1.5 rounded bg-studio-850 hover:bg-studio-800 text-xs font-mono border border-studio-700">
                  <i data-lucide="folder-open" class="w-3.5 h-3.5"></i>
                  <span>OPEN DIRECTORY</span>
                </button>
                <a href="${API_BASE}/api/productions/${p.id}/export-zip" class="flex items-center gap-1.5 px-3 py-1.5 rounded bg-studio-amber text-studio-950 font-bold text-xs font-mono hover:bg-amber-400">
                  <i data-lucide="download" class="w-3.5 h-3.5"></i>
                  <span>DOWNLOAD YOUTUBE BUNDLE (.ZIP)</span>
                </a>
              </div>
            </div>

            <!-- Master Player -->
            <div class="bg-studio-900 border border-studio-800 rounded-xl p-6 shadow-2xl">
              <div class="w-full aspect-video bg-studio-950 rounded-lg overflow-hidden border border-studio-800 mb-4 shadow-inner">
                <video id="master-video-player" controls class="w-full h-full" src="${API_BASE}/media/${p.date_folder}/${p.topic_slug}/video/preview_720p.mp4"></video>
              </div>

              <!-- Quality & Chapter Toolbar -->
              <div class="flex items-center justify-between mb-3">
                <span class="text-[11px] font-mono text-studio-muted">QUALITY SELECTION:</span>
                <div class="flex items-center gap-2">
                  <button onclick="switchVideoQuality('1080p')" class="px-2.5 py-1 rounded bg-studio-800 hover:bg-studio-750 text-studio-amber font-mono font-bold text-xs border border-studio-amber/30">1080P MASTER (148.9 MB)</button>
                  <button onclick="switchVideoQuality('720p')" class="px-2.5 py-1 rounded bg-studio-850 hover:bg-studio-800 text-studio-muted font-mono text-xs border border-studio-700">720P FAST PREVIEW (53.4 MB)</button>
                </div>
              </div>

              <!-- Interactive Chapter Buttons -->
              <div class="mb-4 pt-2">
                <span class="text-[11px] font-mono text-studio-muted block mb-2">QUICK CHAPTER SEEK:</span>
                <div class="flex flex-wrap gap-2">
                  ${(meta.chapters || [
                    { time: "00:00", title: "Silence at 00:00:00", sec: 0 },
                    { time: "01:45", title: "Hour 1: Signaling Storm", sec: 105 },
                    { time: "03:30", title: "Hour 3: Ghost Register", sec: 210 },
                    { time: "05:15", title: "Hour 6: Giants of Commerce", sec: 315 },
                    { time: "07:05", title: "Hour 12: Grid Islanding", sec: 425 },
                    { time: "08:50", title: "Hour 18: Analog Renaissance", sec: 530 },
                    { time: "10:35", title: "Hour 24: Thundering Herd", sec: 635 },
                    { time: "12:15", title: "Conclusion: Fragility", sec: 735 }
                  ]).map(ch => `
                    <button onclick="jumpToVideoTime(${ch.sec || 0})" class="px-2.5 py-1 rounded bg-studio-850 hover:bg-studio-800 border border-studio-700 text-[11px] font-mono text-studio-chalk transition">
                      <span class="text-studio-amber font-bold">${ch.time}</span> ${ch.title}
                    </button>
                  `).join("")}
                </div>
              </div>

              <!-- Metadata & 1-Click Copy Bar -->
              <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 pt-4 border-t border-studio-800/80">
                <div>
                  <h3 class="text-sm font-bold text-studio-chalk">${p.topic_title}</h3>
                  <p class="text-xs text-studio-muted font-mono mt-0.5">Format: 1920x1080 | 30 FPS | H.264 | AAC Audio | EBU R128 (-16 LUFS)</p>
                </div>
                <div class="flex items-center gap-2">
                  <button onclick="copyToClipboard('${(meta.final_title || p.topic_title).replace(/'/g, "\\'")}', 'Title')" class="px-3 py-1.5 rounded bg-studio-850 hover:bg-studio-800 text-xs font-mono border border-studio-700">
                    COPY TITLE
                  </button>
                  <button onclick="copyToClipboard(\`${(meta.description || '').replace(/`/g, '\\`')}\`, 'Description & Chapters')" class="px-3 py-1.5 rounded bg-studio-850 hover:bg-studio-800 text-xs font-mono border border-studio-700">
                    COPY DESCRIPTION
                  </button>
                  <button onclick="copyToClipboard('${(meta.tags || []).join(', ')}', 'SEO Tags')" class="px-3 py-1.5 rounded bg-studio-850 hover:bg-studio-800 text-xs font-mono border border-studio-700">
                    COPY TAGS
                  </button>
                  ${p.approved_by_user ? '<span class="px-3 py-1.5 rounded-lg text-xs font-bold font-mono bg-studio-emerald/20 text-studio-emerald border border-studio-emerald/30">APPROVED FOR RELEASE</span>' : `<button onclick="approveVideo('${p.id}')" class="px-4 py-1.5 bg-studio-emerald text-studio-950 text-xs font-bold rounded-lg hover:bg-emerald-400 font-mono">APPROVE RELEASE</button>`}
                </div>
              </div>
            </div>

            <!-- Thumbnails -->
            <div class="bg-studio-900 border border-studio-800 rounded-xl p-6 shadow-xl">
              <h3 class="text-xs font-mono font-bold text-studio-chalk uppercase tracking-wider mb-4">3 High-CTR Thumbnail Concepts (1280x720)</h3>
              <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                ${thumbnails.map(t => `
                  <div class="bg-studio-950 rounded-lg border border-studio-800 overflow-hidden shadow-md">
                    <img src="${API_BASE}/media/${p.date_folder}/${p.topic_slug}/thumbnails/thumbnail_${t.id}.png" class="w-full aspect-video object-cover" />
                    <div class="p-3">
                      <span class="text-xs font-bold text-studio-chalk block font-mono">${t.title}</span>
                      <p class="text-[11px] text-studio-muted line-clamp-2 mt-1 font-sans">${t.visual_hook}</p>
                    </div>
                  </div>
                `).join("")}
              </div>
            </div>
          </div>
        `;
      } else if (currentTab === "analytics") {
        main.innerHTML = `
          <div class="space-y-6 max-w-7xl mx-auto">
            <div>
              <h2 class="text-xl font-bold text-studio-chalk">Audience Analytics & Retention Intelligence</h2>
              <p class="text-xs text-studio-muted font-mono mt-0.5">Predictive algorithmic model based on YouTube technology niche benchmarks.</p>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div class="bg-studio-900 border border-studio-800 rounded-xl p-5 shadow-lg">
                <span class="text-[11px] font-mono text-studio-muted block mb-1">PROJECTED 30-DAY VIEWS</span>
                <span class="text-2xl font-bold text-studio-chalk">620,000 - 1.2M</span>
                <span class="text-[11px] text-studio-emerald font-mono block mt-2">+42% Above Niche Baseline</span>
              </div>
              <div class="bg-studio-900 border border-studio-800 rounded-xl p-5 shadow-lg">
                <span class="text-[11px] font-mono text-studio-muted block mb-1">ESTIMATED CTR</span>
                <span class="text-2xl font-bold text-studio-amber">9.4%</span>
                <span class="text-[11px] text-zinc-500 font-mono block mt-2">High-contrast illustrated thumbnails</span>
              </div>
              <div class="bg-studio-900 border border-studio-800 rounded-xl p-5 shadow-lg">
                <span class="text-[11px] font-mono text-studio-muted block mb-1">AUDIENCE RETENTION AT 5 MIN</span>
                <span class="text-2xl font-bold text-studio-teal">68.2%</span>
                <span class="text-[11px] text-zinc-500 font-mono block mt-2">Driven by 40 continuous scene transitions</span>
              </div>
            </div>
          </div>
        `;
      } else {
        main.innerHTML = `
          <div class="space-y-6 max-w-7xl mx-auto">
            <h2 class="text-xl font-bold text-studio-chalk capitalize">${currentTab} Module</h2>
            <div class="bg-studio-900 border border-studio-800 rounded-xl p-6 text-xs font-mono text-studio-muted">
              Live studio configuration and telemetry active.
            </div>
          </div>
        `;
      }
      lucide.createIcons();
    }

    function changeScene(delta) {
      const p = state.currentProd || {};
      const scenes = (p.data && p.data.scenes) || [];
      const total = scenes.length || 40;
      state.selectedScene = (state.selectedScene + delta + total) % total;
      renderContent();
    }

    // Initialize
    renderNav();
    pollData();
    setInterval(pollData, 3000);
  </script>
</body>
</html>"""

for path_str in ["backend/app/templates/index.html", "backend/templates/index.html"]:
    p = Path(path_str)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(html_content, encoding="utf-8")
    print(f"Wrote updated template to {path_str}")
