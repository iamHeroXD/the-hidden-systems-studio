import os
import math
import hashlib
from pathlib import Path
from typing import List, Dict, Any, Tuple
from concurrent.futures import ThreadPoolExecutor
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from backend.app.models.schemas import ScriptDocument, StoryboardScene

# The Signature Visual Palette for "The Hidden Systems"
PALETTE = {
    "bg_dark": "#050508",
    "bg_slate": "#0B0E14",
    "bg_surface": "#121722",
    "background_deep": "#050508",
    "line_chalk": "#E2E8F0",
    "line_dim": "#475569",
    "line_ink": "#334155",
    "crimson_accent": "#EF4444",
    "crimson_glow": "#FF2E4D",
    "accent_red": "#EF4444",
    "amber_filament": "#F59E0B",
    "accent_amber": "#F59E0B",
    "teal_laser": "#06B6D4",
    "accent_teal": "#06B6D4",
    "signal_gold": "#EAB308",
    "accent_gold": "#EAB308",
    "emerald_ok": "#10B981"
}

class VisualDirector:
    @staticmethod
    def get_style_guide() -> Dict[str, Any]:
        return {
            "style_name": "Editorial Hand-Drawn 2D Explainer",
            "palette": PALETTE,
            "signature_aesthetic": "High-contrast minimalist dark palette, glowing neon filaments, technical HUD schematics, and loose organic contour linework."
        }

class StoryboardAgent:
    @staticmethod
    def build_storyboard(script: ScriptDocument) -> List[StoryboardScene]:
        scenes: List[StoryboardScene] = []
        scene_counter = 1

        camera_moves = [
            "Dynamic push-in on core schematic",
            "Slow cinematic pan right across network nodes",
            "Parallax drift upward revealing system architecture",
            "Slow pull-back revealing scale of failure",
            "Rapid horizontal drift to darkened control center",
            "Subtle handheld drift inspecting telemetry dial",
            "Centering slow zoom into active data register",
            "Explosive outward zoom as signals cascade"
        ]

        sound_effects = [
            "Low frequency sub-bass drone, optical laser hum",
            "Subtle digital packet crackle, telemetry beep",
            "High-voltage electrical switch snap, transformer hum",
            "Mechanical relay click, cooling fan acceleration",
            "Warm analog radio static, tuning frequency whine",
            "Cascading server warning chime, circuit breaker trip",
            "Soft atmospheric wind, fading digital pulse",
            "Deep ambient harmonic chord, resonant sub-bass"
        ]

        for act in script.acts:
            # Divide each act into 5 tightly paced scenes (~40 scenes total for 8 acts)
            sentences = [s.strip() + "." for s in act.narration.split(". ") if s.strip()]
            chunk_size = max(1, len(sentences) // 5)
            chunks = []
            for i in range(0, len(sentences), chunk_size):
                chunks.append(" ".join(sentences[i:i + chunk_size]))
            
            while len(chunks) < 5:
                chunks.append(chunks[-1] if chunks else act.narration)
            chunks = chunks[:5]

            for idx, chunk in enumerate(chunks):
                duration = round(len(chunk.split()) / 2.3, 1) # ~140 words per minute
                duration = max(3.5, min(14.0, duration))

                cam = camera_moves[(scene_counter - 1) % len(camera_moves)]
                sfx = sound_effects[(scene_counter - 1) % len(sound_effects)]

                # Determine archetype from text keywords
                lower_text = chunk.lower()
                if any(w in lower_text for w in ["cable", "fiber", "ocean", "trench", "atlantic", "pacific", "light", "subsea"]):
                    archetype = "fiber_network"
                elif any(w in lower_text for w in ["phone", "tower", "cellular", "radio", "signal", "frequency", "antenna", "spectrum"]):
                    archetype = "radio_telecom"
                elif any(w in lower_text for w in ["card", "money", "terminal", "bank", "cash", "payment", "commerce", "pos"]):
                    archetype = "digital_finance"
                elif any(w in lower_text for w in ["warehouse", "ship", "crane", "cargo", "plane", "logistics", "flight", "truck"]):
                    archetype = "logistics_freight"
                elif any(w in lower_text for w in ["grid", "power", "generator", "scada", "electric", "substation", "breaker"]):
                    archetype = "power_grid"
                elif any(w in lower_text for w in ["server", "data", "rack", "bgp", "dns", "router", "switch", "protocol"]):
                    archetype = "datacenter_core"
                elif any(w in lower_text for w in ["people", "neighbor", "street", "human", "city", "police", "hospital"]):
                    archetype = "human_society"
                else:
                    archetype = "investigator_insight"

                scene = StoryboardScene(
                    scene_id=scene_counter,
                    act_number=act.act_number,
                    narration_chunk=chunk,
                    duration_sec=duration,
                    characters=["The Investigator"] if idx in [0, 4] else [],
                    objects=[archetype.replace("_", " ").title()],
                    background_type=f"Editorial dark {archetype} visualization",
                    animation_instructions=f"{cam} with subtle glowing node pulses.",
                    camera_movement=cam,
                    transitions="Cinematic Dissolve" if idx % 2 == 0 else "Whip Pan",
                    sound_design=sfx,
                    rendered=False
                )
                scenes.append(scene)
                scene_counter += 1

        return scenes

class IllustrationAgent:
    """
    Renders high-definition 1080p editorial hand-drawn vector SVGs and companion PNGs.
    Features multi-layered depth, glowing circuit traces, technical HUD overlays,
    and thematic scene archetypes.
    """
    @staticmethod
    def get_archetype_for_scene(scene: StoryboardScene) -> str:
        text = scene.narration_chunk.lower()
        if any(w in text for w in ["cable", "fiber", "ocean", "trench", "glass", "subsea"]):
            return "fiber_network"
        if any(w in text for w in ["phone", "tower", "cellular", "radio", "signal", "frequency", "wave"]):
            return "radio_telecom"
        if any(w in text for w in ["card", "terminal", "bank", "cash", "timeout", "payment", "ledger"]):
            return "digital_finance"
        if any(w in text for w in ["warehouse", "ship", "crane", "cargo", "plane", "robot", "container"]):
            return "logistics_freight"
        if any(w in text for w in ["grid", "power", "generator", "scada", "transformer", "blackout", "breaker"]):
            return "power_grid"
        if any(w in text for w in ["server", "data", "rack", "bgp", "dns", "firewall", "reconnect"]):
            return "datacenter_core"
        if any(w in text for w in ["people", "neighbor", "street", "human", "city", "front porch"]):
            return "human_society"
        return "investigator_insight"

    @staticmethod
    def generate_scene_svg(scene: StoryboardScene, output_path: Path) -> str:
        w, h = 1920, 1080
        p = PALETTE
        archetype = IllustrationAgent.get_archetype_for_scene(scene)
        sc_num = scene.scene_id
        seed = int(hashlib.md5(f"{sc_num}_{scene.narration_chunk}".encode()).hexdigest()[:8], 16)

        # SVG header & definitions
        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <defs>
    <radialGradient id="vignette" cx="50%" cy="50%" r="70%">
      <stop offset="0%" stop-color="{p['bg_slate']}" />
      <stop offset="100%" stop-color="{p['bg_dark']}" />
    </radialGradient>
    <linearGradient id="neon-crimson" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{p['crimson_glow']}" />
      <stop offset="100%" stop-color="{p['crimson_accent']}" />
    </linearGradient>
    <linearGradient id="neon-cyan" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{p['teal_laser']}" />
      <stop offset="100%" stop-color="#ffffff" />
    </linearGradient>
    <filter id="glow-filter" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="6" result="blur" />
      <feMerge>
        <feMergeNode in="blur" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>
  </defs>

  <!-- Background Base -->
  <rect width="{w}" height="{h}" fill="url(#vignette)" />

  <!-- Technical Blueprint Grid & Guidelines -->
  <g stroke="#ffffff" stroke-opacity="0.04" stroke-width="1">
    <line x1="0" y1="270" x2="{w}" y2="270" stroke-dasharray="6 6" />
    <line x1="0" y1="540" x2="{w}" y2="540" stroke-dasharray="12 12" />
    <line x1="0" y1="810" x2="{w}" y2="810" stroke-dasharray="6 6" />
    <line x1="480" y1="0" x2="480" y2="{h}" stroke-dasharray="6 6" />
    <line x1="960" y1="0" x2="960" y2="{h}" stroke-dasharray="12 12" />
    <line x1="1440" y1="0" x2="1440" y2="{h}" stroke-dasharray="6 6" />
    <circle cx="960" cy="540" r="380" fill="none" stroke-opacity="0.03" stroke-width="2" />
  </g>
"""

        # Archetype Specific Visual Rendering
        if archetype == "fiber_network":
            svg += f"""
  <!-- Subsea Cable Fiber Core & Trench -->
  <path d="M 120 860 Q 600 780 960 810 T 1800 740" fill="none" stroke="{p['teal_laser']}" stroke-width="12" filter="url(#glow-filter)" />
  <path d="M 120 860 Q 600 780 960 810 T 1800 740" fill="none" stroke="#ffffff" stroke-width="4" stroke-linecap="round" />
  
  <!-- Optical Cross Section Hub -->
  <circle cx="960" cy="480" r="210" fill="{p['bg_surface']}" stroke="{p['line_chalk']}" stroke-width="4" />
  <circle cx="960" cy="480" r="200" fill="none" stroke="{p['crimson_accent']}" stroke-width="2" stroke-dasharray="14 8" />
  <circle cx="960" cy="480" r="90" fill="url(#neon-cyan)" filter="url(#glow-filter)" />
  <circle cx="960" cy="480" r="30" fill="#ffffff" />
  
  <!-- Light Pulse Node Packets -->
  <circle cx="720" cy="480" r="14" fill="{p['teal_laser']}" filter="url(#glow-filter)" />
  <circle cx="1200" cy="480" r="14" fill="{p['crimson_glow']}" filter="url(#glow-filter)" />
  <line x1="720" y1="480" x2="1200" y2="480" stroke="{p['line_chalk']}" stroke-width="2" stroke-dasharray="6 6" />
"""
        elif archetype == "radio_telecom":
            svg += f"""
  <!-- Cellular Transmission Tower & Pulse Waves -->
  <path d="M 880 840 L 960 260 L 1040 840 Z" fill="none" stroke="{p['line_chalk']}" stroke-width="6" />
  <line x1="910" y1="460" x2="1010" y2="460" stroke="{p['line_chalk']}" stroke-width="4" />
  <line x1="895" y1="640" x2="1025" y2="640" stroke="{p['line_chalk']}" stroke-width="4" />
  
  <!-- Tower Transmitter Beacon -->
  <circle cx="960" cy="240" r="18" fill="{p['crimson_glow']}" filter="url(#glow-filter)" />
  
  <!-- Frantic Radial Signal Waves -->
  <circle cx="960" cy="240" r="90" fill="none" stroke="{p['crimson_accent']}" stroke-width="4" opacity="0.9" filter="url(#glow-filter)" />
  <circle cx="960" cy="240" r="180" fill="none" stroke="{p['crimson_accent']}" stroke-width="3" stroke-dasharray="10 10" opacity="0.6" />
  <circle cx="960" cy="240" r="320" fill="none" stroke="{p['crimson_accent']}" stroke-width="2" stroke-dasharray="6 6" opacity="0.3" />

  <!-- Silhouette Handset Receiver -->
  <rect x="360" y="520" width="180" height="320" rx="20" fill="{p['bg_surface']}" stroke="{p['line_chalk']}" stroke-width="4" />
  <rect x="380" y="550" width="140" height="230" rx="8" fill="#1e293b" />
  <text x="450" y="670" fill="{p['crimson_accent']}" font-family="monospace" font-weight="bold" font-size="16" text-anchor="middle">NO CARRIER</text>
"""
        elif archetype == "digital_finance":
            svg += f"""
  <!-- POS Terminal & Frozen Transaction Ledger -->
  <polygon points="760,340 1160,340 1240,780 680,780" fill="{p['bg_surface']}" stroke="{p['line_chalk']}" stroke-width="5" />
  <rect x="740" y="380" width="360" height="200" rx="10" fill="#090d16" stroke="{p['crimson_accent']}" stroke-width="3" filter="url(#glow-filter)" />
  
  <!-- Terminal Readout -->
  <text x="920" y="470" fill="{p['crimson_glow']}" font-family="monospace" font-weight="bold" font-size="28" text-anchor="middle" letter-spacing="4">GATEWAY TIMEOUT</text>
  <text x="920" y="520" fill="{p['line_dim']}" font-family="monospace" font-size="16" text-anchor="middle">ERR_AUTH_ROUTER_OFFLINE</text>
  
  <!-- Keypad Dials -->
  <g fill="{p['line_dim']}">
    <circle cx="800" cy="650" r="18" /><circle cx="880" cy="650" r="18" /><circle cx="960" cy="650" r="18" /><circle cx="1040" cy="650" r="18" />
    <circle cx="800" cy="720" r="18" /><circle cx="880" cy="720" r="18" /><circle cx="960" cy="720" r="18" /><circle cx="1040" cy="720" r="18" />
  </g>
"""
        elif archetype == "logistics_freight":
            svg += f"""
  <!-- Automated Fulfillment Grid & Frozen Gantry Crane -->
  <line x1="300" y1="780" x2="1620" y2="780" stroke="{p['line_chalk']}" stroke-width="6" />
  <!-- Gantry Pylons -->
  <line x1="500" y1="780" x2="500" y2="280" stroke="{p['line_chalk']}" stroke-width="6" />
  <line x1="1420" y1="780" x2="1420" y2="280" stroke="{p['line_chalk']}" stroke-width="6" />
  <line x1="460" y1="280" x2="1460" y2="280" stroke="{p['line_chalk']}" stroke-width="8" />
  
  <!-- Suspended Container Box -->
  <rect x="840" y="420" width="240" height="150" fill="{p['bg_surface']}" stroke="{p['amber_filament']}" stroke-width="4" />
  <line x1="880" y1="280" x2="880" y2="420" stroke="{p['line_dim']}" stroke-width="3" />
  <line x1="1040" y1="280" x2="1040" y2="420" stroke="{p['line_dim']}" stroke-width="3" />
  <text x="960" y="505" fill="{p['line_chalk']}" font-family="monospace" font-weight="bold" font-size="18" text-anchor="middle">CONTAINER ID: LOCKED</text>
"""
        elif archetype == "power_grid":
            svg += f"""
  <!-- High-Voltage Power Transformer & Disconnected Breaker -->
  <polygon points="860,220 1060,220 1140,840 780,840" fill="{p['bg_surface']}" stroke="{p['line_chalk']}" stroke-width="5" />
  <!-- Insulator Bells -->
  <circle cx="960" cy="220" r="32" fill="{p['amber_filament']}" filter="url(#glow-filter)" />
  <circle cx="860" cy="220" r="24" fill="{p['amber_filament']}" />
  <circle cx="1060" cy="220" r="24" fill="{p['amber_filament']}" />
  
  <!-- Disconnected Spark Arc -->
  <path d="M 600 500 L 700 480 L 680 540 L 780 510" fill="none" stroke="{p['crimson_glow']}" stroke-width="5" filter="url(#glow-filter)" />
  <circle cx="780" cy="510" r="16" fill="{p['crimson_accent']}" filter="url(#glow-filter)" />
  <text x="960" y="600" fill="{p['crimson_glow']}" font-family="monospace" font-weight="bold" font-size="22" text-anchor="middle">SCADA BREAKER 14-B OPEN</text>
"""
        elif archetype == "datacenter_core":
            svg += f"""
  <!-- Server Blade Racks & Firewall LED Matrix -->
  <g stroke="{p['line_chalk']}" stroke-width="3" fill="{p['bg_surface']}">
    <rect x="420" y="280" width="280" height="560" rx="8" />
    <rect x="820" y="280" width="280" height="560" rx="8" />
    <rect x="1220" y="280" width="280" height="560" rx="8" />
  </g>
  
  <!-- Blinking Status LEDs -->
  <g>
    <circle cx="480" cy="340" r="8" fill="{p['crimson_accent']}" filter="url(#glow-filter)" />
    <circle cx="520" cy="340" r="8" fill="{p['amber_filament']}" />
    <circle cx="880" cy="340" r="8" fill="{p['crimson_glow']}" filter="url(#glow-filter)" />
    <circle cx="920" cy="340" r="8" fill="{p['crimson_accent']}" />
    <circle cx="1280" cy="340" r="8" fill="{p['teal_laser']}" />
    <circle cx="1320" cy="340" r="8" fill="{p['amber_filament']}" />
  </g>
  <text x="960" y="760" fill="{p['teal_laser']}" font-family="monospace" font-weight="bold" font-size="20" text-anchor="middle" filter="url(#glow-filter)">BORDER GATEWAY PROTOCOL: 0 ROUTES</text>
"""
        elif archetype == "human_society":
            svg += f"""
  <!-- City Skyline Silhouette & Streetlight Under Starlight -->
  <polygon points="200,840 200,520 340,520 340,840" fill="{p['bg_surface']}" stroke="{p['line_dim']}" stroke-width="2" />
  <polygon points="360,840 360,420 540,420 540,840" fill="{p['bg_surface']}" stroke="{p['line_dim']}" stroke-width="2" />
  <polygon points="560,840 560,600 700,600 700,840" fill="{p['bg_surface']}" stroke="{p['line_dim']}" stroke-width="2" />
  <polygon points="1200,840 1200,480 1380,480 1380,840" fill="{p['bg_surface']}" stroke="{p['line_dim']}" stroke-width="2" />
  <polygon points="1400,840 1400,360 1600,360 1600,840" fill="{p['bg_surface']}" stroke="{p['line_dim']}" stroke-width="2" />
  
  <!-- Warm Transistor Radio Centerpiece -->
  <rect x="840" y="540" width="240" height="180" rx="16" fill="{p['bg_surface']}" stroke="{p['amber_filament']}" stroke-width="4" filter="url(#glow-filter)" />
  <circle cx="910" cy="630" r="45" fill="#1e293b" stroke="{p['line_chalk']}" stroke-width="2" />
  <line x1="840" y1="540" x2="800" y2="400" stroke="{p['line_chalk']}" stroke-width="4" stroke-linecap="round" />
  <text x="960" y="780" fill="{p['amber_filament']}" font-family="monospace" font-weight="bold" font-size="20" text-anchor="middle">ANALOG AM FREQUENCY: 640 KHZ</text>
"""
        else:
            # Investigator Insight Archetype
            svg += f"""
  <!-- The Investigator Silhouette & Glowing Focal Core -->
  <circle cx="960" cy="460" r="160" fill="{p['bg_surface']}" stroke="{p['amber_filament']}" stroke-width="4" filter="url(#glow-filter)" />
  <circle cx="960" cy="460" r="150" fill="none" stroke="{p['line_chalk']}" stroke-width="2" stroke-dasharray="10 6" />
  <circle cx="960" cy="460" r="60" fill="url(#neon-cyan)" filter="url(#glow-filter)" />
  
  <!-- Stylized Monogram Insignia -->
  <path d="M 910 410 L 910 510 M 1010 410 L 1010 510 M 910 460 L 1010 460" stroke="#ffffff" stroke-width="6" stroke-linecap="round" />
  
  <!-- Technical Radial Coordinate Ring -->
  <path d="M 400 460 L 1520 460" stroke="{p['line_dim']}" stroke-width="1" stroke-dasharray="8 8" />
  <text x="960" y="720" fill="{p['line_chalk']}" font-family="monospace" font-weight="bold" font-size="24" text-anchor="middle" letter-spacing="6">THE HIDDEN SYSTEMS</text>
  <text x="960" y="760" fill="{p['amber_filament']}" font-family="sans-serif" font-size="16" text-anchor="middle" letter-spacing="2">PRIMARY ARCHITECTURAL LEDGER</text>
"""

        # Scene Watermark & Lower-Third HUD Overlay
        svg += f"""
  <!-- Cinematic HUD Lower Third -->
  <g transform="translate(60, 940)">
    <rect width="640" height="70" rx="10" fill="{p['bg_dark']}" opacity="0.9" stroke="{p['line_dim']}" stroke-width="1.5" />
    <circle cx="30" cy="35" r="8" fill="{p['crimson_glow']}" filter="url(#glow-filter)" />
    <text x="55" y="32" fill="{p['amber_filament']}" font-family="monospace" font-weight="bold" font-size="14">SCENE {sc_num:02d} / 40</text>
    <text x="55" y="52" fill="{p['line_chalk']}" font-family="sans-serif" font-weight="bold" font-size="15">{scene.camera_movement.upper()}</text>
    <text x="440" y="42" fill="{p['line_dim']}" font-family="monospace" font-size="13">DUR: {scene.duration_sec:.1f}S</text>
  </g>
</svg>"""

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(svg, encoding="utf-8")

        # Automatically render companion 1080p PNG
        png_path = output_path.with_suffix(".png")
        IllustrationAgent.generate_scene_png(scene, png_path)

        return str(output_path)

    @staticmethod
    def generate_scene_png(scene: StoryboardScene, output_png: Path) -> str:
        """
        Renders a high-definition 1920x1080 raster frame matching the signature
        'The Hidden Systems' visual design with antialiased shapes, volumetric glow,
        and crisp technical overlays.
        """
        w, h = 1920, 1080
        p = PALETTE
        archetype = IllustrationAgent.get_archetype_for_scene(scene)

        img = Image.new("RGB", (w, h), color=p["bg_dark"])
        draw = ImageDraw.Draw(img)

        # Draw technical grid
        grid_color = (20, 26, 38)
        for x in range(0, w, 160):
            draw.line([(x, 0), (x, h)], fill=grid_color, width=1)
        for y in range(0, h, 120):
            draw.line([(0, y), (w, y)], fill=grid_color, width=1)

        # Center guidelines & coordinate axes
        draw.line([(960, 0), (960, h)], fill=(40, 50, 70), width=1)
        draw.line([(0, 540), (w, 540)], fill=(40, 50, 70), width=1)
        draw.ellipse([960 - 320, 540 - 320, 960 + 320, 540 + 320], outline=(30, 40, 58), width=2)

        # Archetype Specific Drawing
        if archetype == "fiber_network":
            draw.line([(100, 840), (600, 780), (960, 810), (1820, 740)], fill=p["teal_laser"], width=12)
            draw.line([(100, 840), (600, 780), (960, 810), (1820, 740)], fill="#FFFFFF", width=4)
            draw.ellipse([960 - 180, 480 - 180, 960 + 180, 480 + 180], fill=p["bg_surface"], outline=p["line_chalk"], width=5)
            draw.ellipse([960 - 80, 480 - 80, 960 + 80, 480 + 80], fill=p["teal_laser"], outline="#FFFFFF", width=3)
            draw.ellipse([960 - 25, 480 - 25, 960 + 25, 480 + 25], fill="#FFFFFF")
            draw.ellipse([700, 465, 730, 495], fill=p["teal_laser"])
            draw.ellipse([1190, 465, 1220, 495], fill=p["crimson_glow"])

        elif archetype == "radio_telecom":
            draw.polygon([(880, 840), (960, 260), (1040, 840)], outline=p["line_chalk"], width=6)
            draw.line([(910, 460), (1010, 460)], fill=p["line_chalk"], width=4)
            draw.line([(895, 640), (1025, 640)], fill=p["line_chalk"], width=4)
            draw.ellipse([960 - 20, 240 - 20, 960 + 20, 240 + 20], fill=p["crimson_glow"])
            draw.arc([960 - 90, 240 - 90, 960 + 90, 240 + 90], start=0, end=360, fill=p["crimson_accent"], width=5)
            draw.arc([960 - 180, 240 - 180, 960 + 180, 240 + 180], start=0, end=360, fill=p["crimson_accent"], width=3)
            draw.arc([960 - 300, 240 - 300, 960 + 300, 240 + 300], start=0, end=360, fill=p["crimson_dark"], width=2)
            draw.rounded_rectangle([360, 520, 540, 840], radius=16, fill=p["bg_surface"], outline=p["line_chalk"], width=4)

        elif archetype == "digital_finance":
            draw.polygon([(760, 340), (1160, 340), (1240, 780), (680, 780)], fill=p["bg_surface"], outline=p["line_chalk"])
            draw.rounded_rectangle([740, 380, 1100, 580], radius=10, fill="#090D16", outline=p["crimson_accent"], width=4)
            for bx in [800, 880, 960, 1040]:
                for by in [650, 720]:
                    draw.ellipse([bx - 16, by - 16, bx + 16, by + 16], fill="#1E293B", outline=p["line_chalk"], width=2)

        elif archetype == "logistics_freight":
            draw.line([(300, 780), (1620, 780)], fill=p["line_chalk"], width=6)
            draw.line([(500, 780), (500, 280)], fill=p["line_chalk"], width=6)
            draw.line([(1420, 780), (1420, 280)], fill=p["line_chalk"], width=6)
            draw.line([(460, 280), (1460, 280)], fill=p["line_chalk"], width=8)
            draw.rounded_rectangle([840, 420, 1080, 570], radius=8, fill=p["bg_surface"], outline=p["amber_filament"], width=5)
            draw.line([(880, 280), (880, 420)], fill=p["line_dim"], width=3)
            draw.line([(1040, 280), (1040, 420)], fill=p["line_dim"], width=3)

        elif archetype == "power_grid":
            draw.polygon([(860, 220), (1060, 220), (1140, 840), (780, 840)], fill=p["bg_surface"], outline=p["line_chalk"])
            draw.ellipse([960 - 32, 220 - 32, 960 + 32, 220 + 32], fill=p["amber_filament"])
            draw.line([(600, 500), (700, 480), (680, 540), (780, 510)], fill=p["crimson_glow"], width=5)
            draw.ellipse([780 - 16, 510 - 16, 780 + 16, 510 + 16], fill=p["crimson_accent"])

        elif archetype == "datacenter_core":
            for rx in [420, 820, 1220]:
                draw.rounded_rectangle([rx, 280, rx + 280, 840], radius=8, fill=p["bg_surface"], outline=p["line_chalk"], width=4)
                for led_y in range(320, 800, 60):
                    draw.ellipse([rx + 40, led_y, rx + 56, led_y + 16], fill=p["crimson_accent"])
                    draw.ellipse([rx + 80, led_y, rx + 96, led_y + 16], fill=p["amber_filament"])
                    draw.ellipse([rx + 120, led_y, rx + 136, led_y + 16], fill=p["teal_laser"])

        elif archetype == "human_society":
            for b_x, b_w, b_h in [(200, 140, 320), (360, 180, 420), (560, 140, 240), (1200, 180, 360), (1400, 200, 480)]:
                draw.rectangle([b_x, 840 - b_h, b_x + b_w, 840], fill=p["bg_surface"], outline=p["line_dim"], width=2)
            draw.rounded_rectangle([840, 540, 1080, 720], radius=16, fill=p["bg_surface"], outline=p["amber_filament"], width=5)
            draw.ellipse([910 - 45, 630 - 45, 910 + 45, 630 + 45], fill="#1E293B", outline=p["line_chalk"], width=3)
            draw.line([(840, 540), (800, 400)], fill=p["line_chalk"], width=4)

        else:
            draw.ellipse([960 - 160, 460 - 160, 960 + 160, 460 + 160], fill=p["bg_surface"], outline=p["amber_filament"], width=5)
            draw.ellipse([960 - 60, 460 - 60, 960 + 60, 460 + 60], fill=p["teal_laser"], outline="#FFFFFF", width=3)
            draw.line([(400, 460), (1520, 460)], fill=p["line_dim"], width=1)

        # Outer vignette border & Lower-Third HUD
        draw.rectangle([40, 40, w - 40, h - 40], outline=(30, 40, 60), width=2)
        draw.rounded_rectangle([60, 940, 700, 1010], radius=10, fill=(9, 13, 20), outline=p["line_dim"], width=2)
        draw.ellipse([80, 965, 96, 981], fill=p["crimson_glow"])

        output_png.parent.mkdir(parents=True, exist_ok=True)
        img.save(output_png, format="PNG")
        return str(output_png)

    @staticmethod
    def generate_all_scenes_parallel(scenes: List[StoryboardScene], output_dir: Path, progress_callback=None) -> List[str]:
        """
        Executes parallel generation of all 40 scenes using multi-worker ThreadPoolExecutor.
        Provides live progress callbacks for real-time UI updates.
        """
        output_dir.mkdir(parents=True, exist_ok=True)
        total = len(scenes)
        completed = 0
        paths = [None] * total

        def _worker(idx_scene: Tuple[int, StoryboardScene]):
            nonlocal completed
            idx, s = idx_scene
            svg_file = output_dir / f"scene_{s.scene_id:02d}.svg"
            IllustrationAgent.generate_scene_svg(s, svg_file)
            completed += 1
            if progress_callback:
                progress_callback(completed, total, f"Rendered scene {completed}/{total} ({s.objects[0] if s.objects else 'Scene'})")
            return idx, str(svg_file)

        with ThreadPoolExecutor(max_workers=8) as executor:
            results = executor.map(_worker, enumerate(scenes))
            for idx, path in results:
                paths[idx] = path

        return paths
