import os
import math
import hashlib
from pathlib import Path
from typing import List, Dict, Any, Tuple
from concurrent.futures import ThreadPoolExecutor
from PIL import Image, ImageDraw, ImageFont
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
                archetype = IllustrationAgent.get_archetype_for_text(chunk)

                scene = StoryboardScene(
                    scene_id=scene_counter,
                    act_number=act.act_number,
                    narration_chunk=chunk,
                    duration_sec=duration,
                    characters=["The Investigator"] if idx in [0, 4] else [],
                    objects=[archetype.replace("_", " ").title()],
                    background_type=f"Editorial dark {archetype} visualization",
                    animation_instructions=f"{cam} with dynamic scanning beam.",
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
    Renders broadcast-grade 1080p editorial technical vector SVGs and companion raster frames.
    Features 12 distinct technical archetypes, procedural waveforms, telemetry HUD overlays,
    and scene-specific schematic geometry.
    """
    @staticmethod
    def get_archetype_for_text(text: str) -> str:
        t = text.lower()
        if any(w in t for w in ["quantum", "qubit", "rsa", "encryption", "crypto", "algorithm", "shor"]):
            return "quantum_break"
        if any(w in t for w in ["key", "icann", "vault", "safe", "ceremony", "smartcard", "hsm"]):
            return "cryptographic_vault"
        if any(w in t for w in ["cable", "fiber", "ocean", "trench", "atlantic", "pacific", "subsea", "glass"]):
            return "fiber_bathymetry"
        if any(w in t for w in ["bgp", "router", "route", "internet", "traffic", "prefix", "dns", "autonomous"]):
            return "bgp_routing_anomaly"
        if any(w in t for w in ["power", "grid", "transformer", "scada", "generator", "substation", "breaker", "voltage"]):
            return "power_scada_blackout"
        if any(w in t for w in ["phone", "cellular", "tower", "radio", "signal", "frequency", "wave", "3gpp"]):
            return "cellular_signaling_storm"
        if any(w in t for w in ["bank", "card", "terminal", "money", "cash", "payment", "swift", "fedwire", "pos"]):
            return "digital_settlement_ledger"
        if any(w in t for w in ["freight", "warehouse", "cargo", "ship", "crane", "plane", "logistics", "flight"]):
            return "intermodal_freight_hub"
        if any(w in t for w in ["server", "rack", "datacenter", "cooling", "patch", "chassis"]):
            return "datacenter_thermal_core"
        if any(w in t for w in ["analog", "am", "dial", "transistor", "conelrad", "vacuum"]):
            return "analog_conelrad_broadcast"
        if any(w in t for w in ["people", "city", "society", "hospital", "police", "human", "street"]):
            return "human_civilization_silhouette"
        return "investigative_ledger"

    @staticmethod
    def generate_scene_svg(scene: StoryboardScene, output_path: Path) -> str:
        w, h = 1920, 1080
        p = PALETTE
        archetype = IllustrationAgent.get_archetype_for_text(scene.narration_chunk)
        sc_num = scene.scene_id

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
  </defs>

  <rect width="{w}" height="{h}" fill="url(#vignette)" />
  <g stroke="#ffffff" stroke-opacity="0.04" stroke-width="1">
    <line x1="0" y1="270" x2="{w}" y2="270" stroke-dasharray="6 6" />
    <line x1="0" y1="540" x2="{w}" y2="540" stroke-dasharray="12 12" />
    <line x1="0" y1="810" x2="{w}" y2="810" stroke-dasharray="6 6" />
    <line x1="960" y1="0" x2="960" y2="{h}" stroke-dasharray="12 12" />
  </g>
  <text x="960" y="540" fill="{p['crimson_accent']}" font-family="monospace" font-size="32" text-anchor="middle">THE HIDDEN SYSTEMS // SCENE {sc_num:02d}</text>
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
        Renders a broadcast-grade 1920x1080 master raster frame.
        Features unique procedural schematics, live waveforms, technical HUD, and typography.
        """
        w, h = 1920, 1080
        p = PALETTE
        archetype = IllustrationAgent.get_archetype_for_text(scene.narration_chunk)
        sc_num = scene.scene_id
        seed = int(hashlib.md5(f"{sc_num}_{scene.narration_chunk}".encode()).hexdigest()[:8], 16)

        # Load crisp Windows system fonts with safe fallbacks
        try:
            font_title = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 30)
            font_hud = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 17)
            font_hud_sm = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 13)
            font_narr = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 22)
            font_narr_bold = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 15)
        except Exception:
            font_title = font_hud = font_hud_sm = font_narr = font_narr_bold = ImageFont.load_default()

        img = Image.new("RGB", (w, h), color=p["bg_dark"])
        draw = ImageDraw.Draw(img)

        # 1. Technical Blueprint Grid & Guidelines
        grid_color = (18, 24, 34)
        for x in range(0, w, 120):
            draw.line([(x, 0), (x, h)], fill=grid_color, width=1)
        for y in range(0, h, 90):
            draw.line([(0, y), (w, y)], fill=grid_color, width=1)

        # Primary Coordinate Crosshairs & Radial Reticles
        draw.line([(960, 0), (960, h)], fill=(30, 40, 58), width=1)
        draw.line([(0, 540), (w, 540)], fill=(30, 40, 58), width=1)
        draw.ellipse([960 - 360, 540 - 360, 960 + 360, 540 + 360], outline=(28, 38, 54), width=2)
        draw.ellipse([960 - 180, 540 - 180, 960 + 180, 540 + 180], outline=(40, 55, 80), width=1)

        # 2. Top Telemetry Header HUD
        draw.rounded_rectangle([50, 36, w - 50, 102], radius=8, fill=(8, 11, 16), outline=(32, 42, 60), width=1)
        draw.ellipse([72, 60, 88, 76], fill=p["crimson_glow"])
        draw.text((102, 48), "THE HIDDEN SYSTEMS // AUTONOMOUS DOCUMENTARY LEDGER", fill=p["crimson_accent"], font=font_hud)
        draw.text((102, 73), f"ACT 0{scene.act_number} // SCENE {sc_num:02d} OF 40 // ARCHETYPE: {archetype.upper().replace('_', ' ')}", fill="#E2E8F0", font=font_hud_sm)
        
        telemetry_txt = f"SYS.TIME 00:{sc_num * 18:02d} // FREQ: 1420 MHZ // ENCRYPT: 4096-RSA"
        draw.text((w - 560, 60), telemetry_txt, fill=p["amber_filament"], font=font_hud_sm)

        # 3. Archetype-Specific Rich Vector Illustration
        if archetype == "quantum_break":
            # Superconducting Qubit Lattice & Bloch Sphere Projection
            for qx in range(720, 1260, 120):
                for qy in range(320, 640, 100):
                    draw.rectangle([qx - 25, qy - 25, qx + 25, qy + 25], fill="#0A101D", outline=p["teal_laser"], width=2)
                    draw.ellipse([qx - 6, qy - 6, qx + 6, qy + 6], fill="#FFFFFF")
                    draw.line([(qx + 25, qy), (qx + 95, qy)], fill=p["line_dim"], width=2)
                    draw.line([(qx, qy + 25), (qx, qy + 75)], fill=p["line_dim"], width=2)
            # Center Bloch Sphere Coordinate Ring
            draw.ellipse([960 - 160, 480 - 160, 960 + 160, 480 + 160], outline=p["crimson_accent"], width=3)
            draw.line([(960 - 160, 480), (960 + 160, 480)], fill=p["teal_laser"], width=2)
            draw.line([(960, 480 - 160), (960, 480 + 160)], fill=p["amber_filament"], width=2)
            draw.line([(960, 480), (1070, 390)], fill="#FFFFFF", width=4)
            draw.ellipse([1070 - 8, 390 - 8, 1070 + 8, 390 + 8], fill=p["crimson_glow"])
            draw.text((960, 710), "SUPERCONDUCTING QUANTUM REGISTER // ERROR RATE: 0.0014%", fill=p["teal_laser"], font=font_hud, anchor="mm")

        elif archetype == "cryptographic_vault":
            # Safe Deposit Keyway & Tamper-Evident HSM Chassis
            draw.rounded_rectangle([720, 280, 1200, 680], radius=20, fill=p["bg_surface"], outline=p["line_chalk"], width=5)
            draw.ellipse([960 - 110, 480 - 110, 960 + 110, 480 + 110], fill="#080C14", outline=p["amber_filament"], width=6)
            for angle in range(0, 360, 30):
                rad = math.radians(angle)
                x1 = 960 + int(math.cos(rad) * 90)
                y1 = 480 + int(math.sin(rad) * 90)
                x2 = 960 + int(math.cos(rad) * 105)
                y2 = 480 + int(math.sin(rad) * 105)
                draw.line([(x1, y1), (x2, y2)], fill=p["line_chalk"], width=3)
            # Keyhole slit
            draw.ellipse([960 - 18, 460 - 18, 960 + 18, 460 + 18], fill=p["crimson_glow"])
            draw.polygon([(948, 460), (972, 460), (966, 520), (954, 520)], fill=p["crimson_glow"])
            draw.text((960, 710), "DNSSEC ROOT KEY VAULT // QUORUM: 3 OF 7 PHYSICAL KEYHOLDERS", fill=p["amber_filament"], font=font_hud, anchor="mm")

        elif archetype == "fiber_bathymetry":
            # Subsea Bathymetry Contour & High-Power Optical Core
            draw.line([(100, 840), (550, 780), (960, 810), (1820, 740)], fill=p["teal_laser"], width=12)
            draw.line([(100, 840), (550, 780), (960, 810), (1820, 740)], fill="#FFFFFF", width=4)
            # Multi-layer Cable Cross Section Hub
            draw.ellipse([960 - 190, 470 - 190, 960 + 190, 470 + 190], fill=p["bg_surface"], outline=p["line_chalk"], width=4)
            draw.ellipse([960 - 140, 470 - 140, 960 + 140, 470 + 140], outline=p["amber_filament"], width=3)
            draw.ellipse([960 - 90, 470 - 90, 960 + 90, 470 + 90], fill=p["teal_laser"], outline="#FFFFFF", width=3)
            draw.ellipse([960 - 30, 470 - 30, 960 + 30, 470 + 30], fill="#FFFFFF")
            # Satellite Repeaters
            draw.ellipse([640, 455, 680, 495], fill=p["teal_laser"], outline="#FFFFFF", width=2)
            draw.ellipse([1240, 455, 1280, 495], fill=p["crimson_glow"], outline="#FFFFFF", width=2)
            draw.line([(680, 475), (1240, 475)], fill=p["line_dim"], width=2)
            draw.text((960, 710), "TRANSOCEANIC OPTICAL BACKBONE: 99.4% GLOBAL TRAFFIC", fill=p["teal_laser"], font=font_hud, anchor="mm")

        elif archetype == "bgp_routing_anomaly":
            # Multi-Node Autonomous System (AS) Topology Map
            nodes = [
                (680, 360, "AS-17557"), (960, 310, "AS-3356"), (1240, 370, "AS-701"),
                (800, 520, "AS-1299"), (1120, 510, "AS-2914"), (960, 640, "AS-6939")
            ]
            for i, (nx, ny, nlabel) in enumerate(nodes):
                for j, (ox, oy, _) in enumerate(nodes):
                    if i < j and ((i + j + seed) % 3 != 0):
                        line_color = p["crimson_accent"] if (i + j) % 4 == 0 else p["line_dim"]
                        draw.line([(nx, ny), (ox, oy)], fill=line_color, width=2)
            for nx, ny, nlabel in nodes:
                is_failed = "17557" in nlabel or "3356" in nlabel
                ncolor = p["crimson_glow"] if is_failed else p["teal_laser"]
                draw.ellipse([nx - 36, ny - 36, nx + 36, ny + 36], fill=p["bg_surface"], outline=ncolor, width=3)
                draw.ellipse([nx - 10, ny - 10, nx + 10, ny + 10], fill=ncolor)
                draw.text((nx, ny + 46), nlabel, fill="#E2E8F0", font=font_hud_sm, anchor="mm")
            draw.text((960, 720), "BORDER GATEWAY PROTOCOL // GLOBAL ROUTE WITHDRAWAL", fill=p["crimson_accent"], font=font_hud, anchor="mm")

        elif archetype == "power_scada_blackout":
            # High-Voltage Substation Transformer & Disconnected Breaker
            draw.polygon([(840, 200), (1080, 200), (1160, 800), (760, 800)], fill=p["bg_surface"], outline=p["line_chalk"], width=4)
            draw.ellipse([960 - 36, 200 - 36, 960 + 36, 200 + 36], fill=p["amber_filament"])
            # Electric Arc Discharge
            draw.line([(580, 470), (690, 440), (670, 510), (780, 480)], fill=p["crimson_glow"], width=6)
            draw.ellipse([780 - 18, 480 - 18, 780 + 18, 480 + 18], fill=p["crimson_accent"])
            draw.text((960, 590), "SCADA BREAKER 14-B TRIPPED", fill=p["crimson_glow"], font=font_title, anchor="mm")
            draw.text((960, 710), "GRID FREQUENCY: 58.14 HZ // DRIFT: -1.86 HZ [CRITICAL]", fill=p["amber_filament"], font=font_hud, anchor="mm")

        elif archetype == "cellular_signaling_storm":
            # Cellular Transmission Pylon & Pulse Wavefronts
            draw.polygon([(880, 820), (960, 230), (1040, 820)], outline=p["line_chalk"], width=5)
            draw.line([(910, 430), (1010, 430)], fill=p["line_chalk"], width=4)
            draw.line([(895, 610), (1025, 610)], fill=p["line_chalk"], width=4)
            draw.ellipse([960 - 24, 230 - 24, 960 + 24, 230 + 24], fill=p["crimson_glow"])
            draw.arc([960 - 120, 230 - 120, 960 + 120, 230 + 120], start=0, end=360, fill=p["crimson_accent"], width=5)
            draw.arc([960 - 240, 230 - 240, 960 + 240, 230 + 240], start=0, end=360, fill=p["crimson_accent"], width=3)
            # Handheld Receiver Silhouette
            draw.rounded_rectangle([360, 480, 540, 800], radius=20, fill=p["bg_surface"], outline=p["line_chalk"], width=4)
            draw.rounded_rectangle([380, 510, 520, 740], radius=8, fill="#050811")
            draw.text((450, 625), "NO CARRIER", fill=p["crimson_glow"], font=font_hud_sm, anchor="mm")
            draw.text((960, 710), "3GPP CELLULAR SIGNALING STORM: RADIO CHANNELS SATURATED", fill=p["crimson_accent"], font=font_hud, anchor="mm")

        elif archetype == "digital_settlement_ledger":
            # Transaction Terminal & Disconnected Ledger
            draw.polygon([(740, 310), (1180, 310), (1260, 740), (660, 740)], fill=p["bg_surface"], outline=p["line_chalk"], width=4)
            draw.rounded_rectangle([720, 350, 1120, 550], radius=12, fill="#060910", outline=p["crimson_accent"], width=4)
            draw.text((920, 430), "GATEWAY TIMEOUT: 504", fill=p["crimson_glow"], font=font_title, anchor="mm")
            draw.text((920, 480), "LEDGER DESYNCHRONIZED // 0 CLEARED TRANSACTIONS", fill=p["amber_filament"], font=font_hud_sm, anchor="mm")
            for bx in [780, 860, 940, 1020]:
                for by in [610, 675]:
                    draw.ellipse([bx - 16, by - 16, bx + 16, by + 16], fill="#1E293B", outline=p["line_chalk"], width=2)
            draw.text((960, 710), "SWIFT & FEDWIRE HIGH-VALUE SETTLEMENT SUSPENDED", fill=p["amber_filament"], font=font_hud, anchor="mm")

        elif archetype == "intermodal_freight_hub":
            # Gantry Crane & Intermodal Container Hub
            draw.line([(280, 780), (1640, 780)], fill=p["line_chalk"], width=6)
            draw.line([(480, 780), (480, 260)], fill=p["line_chalk"], width=6)
            draw.line([(1440, 780), (1440, 260)], fill=p["line_chalk"], width=6)
            draw.line([(440, 260), (1480, 260)], fill=p["line_chalk"], width=8)
            draw.rounded_rectangle([820, 390, 1100, 550], radius=10, fill=p["bg_surface"], outline=p["amber_filament"], width=5)
            draw.line([(860, 260), (860, 390)], fill=p["line_dim"], width=3)
            draw.line([(1060, 260), (1060, 390)], fill=p["line_dim"], width=3)
            draw.text((960, 470), "CONTAINER #HS-9942 LOCKED", fill="#FFFFFF", font=font_hud, anchor="mm")
            draw.text((960, 710), "JUST-IN-TIME FREIGHT CORRIDORS HALTED AT INLAND HUBS", fill=p["amber_filament"], font=font_hud, anchor="mm")

        elif archetype == "datacenter_thermal_core":
            # Server Blade Racks & Fiber Patch Bay
            for rx in [380, 820, 1260]:
                draw.rounded_rectangle([rx, 250, rx + 280, 800], radius=8, fill=p["bg_surface"], outline=p["line_chalk"], width=4)
                for led_y in range(290, 760, 48):
                    draw.ellipse([rx + 35, led_y, rx + 49, led_y + 14], fill=p["crimson_accent"])
                    draw.ellipse([rx + 75, led_y, rx + 89, led_y + 14], fill=p["amber_filament"])
                    draw.ellipse([rx + 115, led_y, rx + 129, led_y + 14], fill=p["teal_laser"])
            draw.text((960, 710), "BORDER GATEWAY PROTOCOL: 0 ROUTES IN GLOBAL RIB", fill=p["teal_laser"], font=font_hud, anchor="mm")

        elif archetype == "analog_conelrad_broadcast":
            # Transistor Radio & Cathode Ray Frequency Glow
            draw.rounded_rectangle([760, 330, 1160, 680], radius=16, fill=p["bg_surface"], outline=p["amber_filament"], width=5)
            draw.ellipse([960 - 90, 490 - 90, 960 + 90, 490 + 90], fill="#080D18", outline=p["line_chalk"], width=3)
            # Tuning pointer
            draw.line([(960, 490), (1020, 440)], fill=p["crimson_glow"], width=4)
            draw.line([(760, 330), (710, 180)], fill=p["line_chalk"], width=4)
            draw.text((960, 710), "EMERGENCY BROADCAST SYSTEM // 640 KHZ CONELRAD", fill=p["amber_filament"], font=font_hud, anchor="mm")

        elif archetype == "human_civilization_silhouette":
            # Metropolitan City Skyline Silhouette & Solitary Beacon
            for b_x, b_w, b_h in [(180, 150, 340), (350, 190, 440), (560, 150, 260), (1210, 190, 380), (1420, 210, 500)]:
                draw.rectangle([b_x, 800 - b_h, b_x + b_w, 800], fill=p["bg_surface"], outline=p["line_dim"], width=2)
            draw.ellipse([960 - 70, 520 - 70, 960 + 70, 520 + 70], fill=p["crimson_glow"])
            draw.text((960, 710), "CIVIL INFRASTRUCTURE DEPENDENCY THRESHOLD EXCEEDED", fill="#FFFFFF", font=font_hud, anchor="mm")

        else:
            # Forensic System Dependency Nexus
            draw.ellipse([960 - 180, 460 - 180, 960 + 180, 460 + 180], fill=p["bg_surface"], outline=p["amber_filament"], width=5)
            draw.ellipse([960 - 80, 460 - 80, 960 + 80, 460 + 80], fill=p["teal_laser"], outline="#FFFFFF", width=3)
            draw.line([(350, 460), (1570, 460)], fill=p["line_dim"], width=1)
            draw.text((960, 710), "SYSTEM ARCHITECTURE: HIDDEN DEPENDENCY MAP", fill="#FFFFFF", font=font_title, anchor="mm")

        # 4. Lower-Right Live Oscilloscope / Signal Waveform Box
        osc_x, osc_y, osc_w, osc_h = w - 420, h - 300, 360, 140
        draw.rounded_rectangle([osc_x, osc_y, osc_x + osc_w, osc_y + osc_h], radius=8, fill=(6, 9, 14), outline=(30, 42, 60), width=1)
        draw.text((osc_x + 12, osc_y + 8), f"SIGNAL TELEMETRY // CHAN {(sc_num % 8) + 1}", fill=p["teal_laser"], font=font_hud_sm)
        # Draw dynamic waveform points
        wave_pts = []
        freq_mult = 0.03 + ((sc_num % 5) * 0.015)
        for px in range(osc_x + 10, osc_x + osc_w - 10, 3):
            rel_x = px - osc_x
            wy = (osc_y + 75) + int(math.sin((rel_x + seed) * freq_mult) * 28 + math.cos(rel_x * 0.07) * 12)
            wave_pts.append((px, wy))
        if len(wave_pts) > 1:
            draw.line(wave_pts, fill=p["teal_laser"], width=2)

        # 5. Cinematic Documentary Lower-Third HUD
        narr_text = scene.narration_chunk.strip()
        if len(narr_text) > 130:
            narr_text = narr_text[:127] + "..."

        draw.rounded_rectangle([50, 875, w - 50, 1015], radius=12, fill=(8, 11, 16), outline=p["crimson_accent"], width=2)
        draw.ellipse([75, 903, 89, 917], fill=p["crimson_glow"])
        draw.text((105, 894), f"SCENE {sc_num:02d} // CAMERA: {scene.camera_movement.upper()} // SOUND: {scene.sound_design[:35].upper()}", fill=p["amber_filament"], font=font_narr_bold)
        draw.text((105, 935), f'"{narr_text}"', fill="#FFFFFF", font=font_narr)

        # Outer Frame Vignette Border
        draw.rectangle([18, 18, w - 18, h - 18], outline=(28, 38, 54), width=1)

        output_png.parent.mkdir(parents=True, exist_ok=True)
        img.save(output_png, format="PNG")
        return str(output_png)

    @staticmethod
    def generate_all_scenes_parallel(scenes: List[StoryboardScene], output_dir: Path, progress_callback=None) -> List[str]:
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
