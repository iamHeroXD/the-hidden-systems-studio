import re
from pathlib import Path

app_template = Path("backend/app/templates/index.html")
content = app_template.read_text(encoding="utf-8")

# 1. Add modal container before toast
modal_html = """
  <!-- Scene Inspection Lightbox Modal -->
  <div id="scene-modal" class="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 hidden flex items-center justify-center p-4">
    <div class="bg-studio-900 border border-studio-700 rounded-2xl max-w-4xl w-full max-h-[90vh] overflow-y-auto p-6 shadow-2xl relative">
      <button onclick="closeSceneModal()" class="absolute top-4 right-4 text-studio-muted hover:text-studio-chalk p-1">
        <i data-lucide="x" class="w-5 h-5"></i>
      </button>
      <div id="scene-modal-content"></div>
    </div>
  </div>
"""

if 'id="scene-modal"' not in content:
    content = content.replace('<!-- Notification Toast Container -->', modal_html + '\n  <!-- Notification Toast Container -->')

# 2. Add JavaScript functions for modal & quality switcher
js_helpers = """
    state.modalSceneIndex = 0;

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
      modalContent.innerHTML = `
        <div class="space-y-4">
          <div class="flex items-center justify-between pr-8">
            <div>
              <span class="px-2 py-0.5 rounded bg-studio-amber/20 text-studio-amber text-xs font-mono font-bold border border-studio-amber/30">
                SCENE ${scNum} / ${scenes.length || 40}
              </span>
              <h3 class="text-base font-bold text-studio-chalk mt-1">${s.visual_prompt || "Scene Artwork"}</h3>
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
      showToast(`Switched player to ${res.toUpperCase()} quality`);
    }
"""

if 'function renderSceneModal' not in content:
    content = content.replace('function showToast(msg) {', js_helpers + '\n    function showToast(msg) {"')

# 3. Enhance Storyboard card button so clicking opens the Lightbox Modal directly
content = content.replace(
    """<button onclick="state.selectedScene = ${s.scene_id - 1}; selectTab('animation');" class="w-full py-1 rounded bg-studio-850 hover:bg-studio-800 text-studio-chalk text-center transition border border-studio-700">
                            INSPECT ANIMATION
                          </button>""",
    """<div class="flex gap-2">
                            <button onclick="openSceneModal(${s.scene_id - 1})" class="flex-1 py-1 rounded bg-studio-850 hover:bg-studio-800 text-studio-amber font-semibold text-center transition border border-studio-700">
                              LIGHTBOX
                            </button>
                            <button onclick="state.selectedScene = ${s.scene_id - 1}; selectTab('animation');" class="flex-1 py-1 rounded bg-studio-900 hover:bg-studio-850 text-studio-chalk text-center transition border border-studio-700">
                              ANIMATION
                            </button>
                          </div>"""
)

# 4. Enhance Video Library player with 1080p / 720p switcher
content = content.replace(
    """<span class="text-[11px] font-mono text-studio-muted block mb-2">QUICK CHAPTER SEEK:</span>""",
    """<div class="flex items-center justify-between mb-3">
                  <span class="text-[11px] font-mono text-studio-muted">QUALITY SELECTION:</span>
                  <div class="flex items-center gap-2">
                    <button onclick="switchVideoQuality('1080p')" class="px-2.5 py-1 rounded bg-studio-800 hover:bg-studio-750 text-studio-amber font-mono font-bold text-xs border border-studio-amber/30">1080P MASTER (148.9 MB)</button>
                    <button onclick="switchVideoQuality('720p')" class="px-2.5 py-1 rounded bg-studio-850 hover:bg-studio-800 text-studio-muted font-mono text-xs border border-studio-700">720P FAST PREVIEW (53.4 MB)</button>
                  </div>
                </div>
                <span class="text-[11px] font-mono text-studio-muted block mb-2">QUICK CHAPTER SEEK:</span>"""
)

app_template.write_text(content, encoding="utf-8")
Path("backend/templates/index.html").write_text(content, encoding="utf-8")
print("Templates enhanced successfully!")
