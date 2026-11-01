import os
from pathlib import Path
from typing import List, Dict, Any
from backend.app.models.schemas import ScriptDocument, StoryboardScene

# The Signature Visual Palette for "The Hidden Systems"
PALETTE = {
    "background_deep": "#0B0F17",       # Ink Midnight
    "background_elevated": "#151C28",   # Deep Slate
    "line_ink": "#E2E8F0",              # Chalk Off-White
    "accent_amber": "#F59E0B",          # Warning Copper / Filament Amber
    "accent_teal": "#06B6D4",           # Subsea Glass Laser Teal
    "accent_red": "#EF4444",            # System Failure Crimson
    "accent_gold": "#EAB308",           # Analog Signal Gold
    "paper_tone": "#F8FAFC",            # Warm Cream
    "shadow_shade": "#030712"           # Obsidian Shadow
}

class VisualDirector:
    @staticmethod
    def get_style_guide() -> Dict[str, Any]:
        return {
            "style_name": "Editorial Hand-Drawn 2D Explainer",
            "line_weight": 2.5,
            "roughness": 1.2,
            "bowing": 1.5,
            "palette": PALETTE,
            "character_lead": {
                "name": "The Investigator",
                "appearance": "Minimalist hand-drawn silhouette with rolled-up sleeves, field trench coat, notebook, and observant posture.",
                "proportions": "Editorial caricature, expressive hands, organic loose linework."
            }
        }

class StoryboardAgent:
    @staticmethod
    def build_storyboard(script: ScriptDocument) -> List[StoryboardScene]:
        scenes: List[StoryboardScene] = []
        scene_counter = 1

        # Camera movements & sound design library
        camera_moves = [
            "Slow cinematic pan right across cable lines",
            "Dynamic push-in on optical fiber core",
            "Parallax drift upward revealing radio tower",
            "Slow pull-back from frozen POS terminal",
            "Rapid horizontal whip-pan to darkened container port",
            "Subtle handheld drift inside emergency power room",
            "Centering slow zoom into transistor radio dial",
            "Explosive outward zoom as network packets surge",
            "Gentle floating crane shot over silent city rooftops"
        ]

        sound_effects = [
            "Subsea ocean rumble, laser optical hum",
            "Subtle static crackle, digital packet beep",
            "Card swipe chime, sharp buzzer error tone",
            "Heavy industrial brake hiss, hydraulic halt",
            "Low frequency electrical transformer hum, switchboard snap",
            "Warm analog radio static, tuning frequency whine",
            "Cascading relay clicks, server fan acceleration",
            "Soft wind across rooftops, fading digital chime"
        ]

        for act in script.acts:
            # Divide each act's narration into 5 tightly paced visual scenes (~40 scenes total)
            sentences = [s.strip() + "." for s in act.narration.split(". ") if s.strip()]
            chunk_size = max(1, len(sentences) // 5)
            chunks = []
            for i in range(0, len(sentences), chunk_size):
                chunks.append(" ".join(sentences[i:i + chunk_size]))
            
            # Ensure exactly 5 scenes per act (total = 40 scenes for 8 acts)
            while len(chunks) < 5:
                chunks.append(chunks[-1] if chunks else act.narration)
            chunks = chunks[:5]

            for idx, chunk in enumerate(chunks):
                duration = round(len(chunk.split()) / 2.4, 1) # ~145 words per minute
                duration = max(3.5, min(12.0, duration))

                cam = camera_moves[(scene_counter - 1) % len(camera_moves)]
                sfx = sound_effects[(scene_counter - 1) % len(sound_effects)]

                if act.act_number == 1:
                    chars = ["The Investigator"] if idx in [0, 4] else []
                    objs = ["Undersea fiber optic cable", "Glass core cross-section", "BGP core router"]
                    bg = "Abyssal Pacific ocean floor with glowing blue fiber strands"
                    anim = "Pulsing photons traveling through glass, suddenly stuttering and going dark."
                elif act.act_number == 2:
                    chars = ["Sleepy resident", "The Investigator"]
                    objs = ["Smartphone screen", "Cellular base station", "Atomic clock symbol"]
                    bg = "Suburban bedroom transitioning to hilltop cellular antenna"
                    anim = "Red signaling waves bursting from phone into tower, tower flashing overload warning."
                elif act.act_number == 3:
                    chars = ["Customer with wallet", "Stressed store cashier"]
                    objs = ["Credit card terminal", "Gas pump nozzle", "Prescription medicine bottles"]
                    bg = "Fluorescent convenience store counter"
                    anim = "Terminal display pulsing 'TIMEOUT', cashier shrugging, analog cash register drawer jamming."
                elif act.act_number == 4:
                    chars = ["Logistics operator", "Cargo crane technician"]
                    objs = ["Kiva automated robot", "Container crane", "Boeing airliner cockpit"]
                    bg = "Vast darkened Amazon fulfillment center and container ship deck"
                    anim = "Robotic orange carriers skidding to an abrupt stop, crane cables swinging motionless in breeze."
                elif act.act_number == 5:
                    chars = ["Grid dispatcher in hard hat"]
                    objs = ["SCADA monitor dials", "High-voltage transformer", "Diesel generator exhaust"]
                    bg = "Regional transmission control room with blinking green/red mosaic wall"
                    anim = "Dials fluctuating wildly, breaker switch dropping with spark, control room lights switching to emergency red."
                elif act.act_number == 6:
                    chars = ["Neighborhood crowd", "Radio host at microphone", "The Investigator"]
                    objs = ["AM transistor radio", "Handwritten paper notice", "Megaphone"]
                    bg = "Neighborhood street corner under brilliant starry night sky"
                    anim = "Radio vacuum tube glowing warm amber, analog soundwaves rippling gently over front porches."
                elif act.act_number == 7:
                    chars = ["Server technician", "The Investigator"]
                    objs = ["Server blade rack", "BGP route matrix diagram", "Traffic graph gauge"]
                    bg = "Subterranean carrier hotel data center with glowing LED arrays"
                    anim = "LED indicators turning from red to amber to blue; network graph spiking past maximum limit."
                else:
                    chars = ["The Investigator"]
                    objs = ["Glowing fiber filament held in hand", "World silhouette", "Channel emblem"]
                    bg = "Minimalist ink backdrop with delicate copper line art"
                    anim = "The Investigator holds glowing fiber strand to the camera; slow dissolve into channel insignia."

                scene = StoryboardScene(
                    scene_id=scene_counter,
                    act_number=act.act_number,
                    narration_chunk=chunk,
                    duration_sec=duration,
                    characters=chars,
                    objects=objs,
                    background_type=bg,
                    animation_instructions=anim,
                    camera_movement=cam,
                    transitions="Sketch reveal wipe" if idx % 2 == 0 else "Crossfade",
                    sound_design=sfx,
                    rendered=False
                )
                scenes.append(scene)
                scene_counter += 1

        return scenes

class IllustrationAgent:
    @staticmethod
    def generate_scene_svg(scene: StoryboardScene, output_path: Path) -> str:
        """
        Generates high-definition, 1080p hand-drawn editorial SVG visuals.
        Employs sketchy double-stroke aesthetics, textured shadows, and organic vector elements.
        """
        w, h = 1920, 1080
        p = PALETTE

        # Procedural sketch elements tailored to the scene context
        svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <defs>
    <filter id="sketch-filter" x="-10%" y="-10%" width="120%" height="120%">
      <feTurbulence type="fractalNoise" baseFrequency="0.04" numOctaves="3" result="noise" />
      <feDisplacementMap in="SourceGraphic" in2="noise" scale="3.5" xChannelSelector="R" yChannelSelector="G" />
    </filter>
    <linearGradient id="bg-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{p['background_deep']}" />
      <stop offset="100%" stop-color="{p['background_elevated']}" />
    </linearGradient>
    <linearGradient id="laser-glow" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{p['accent_teal']}" stop-opacity="0.9" />
      <stop offset="50%" stop-color="#ffffff" stop-opacity="1" />
      <stop offset="100%" stop-color="{p['accent_amber']}" stop-opacity="0.8" />
    </linearGradient>
  </defs>

  <!-- Background Base -->
  <rect width="{w}" height="{h}" fill="url(#bg-grad)" />

  <!-- Subtle Editorial Grid & Technical Guidelines -->
  <g stroke="#ffffff" stroke-opacity="0.04" stroke-width="1" stroke-dasharray="8 8">
    <line x1="0" y1="270" x2="{w}" y2="270" />
    <line x1="0" y1="540" x2="{w}" y2="540" />
    <line x1="0" y1="810" x2="{w}" y2="810" />
    <line x1="480" y1="0" x2="480" y2="{h}" />
    <line x1="960" y1="0" x2="960" y2="{h}" />
    <line x1="1440" y1="0" x2="1440" y2="{h}" />
  </g>

  <!-- Scene Specific Vector Artwork with Hand-Drawn Linework -->
  <g filter="url(#sketch-filter)">
"""

        # Scene context artwork branching
        act = scene.act_number
        if act == 1:
            # Undersea fiber optic cable glowing across abyssal trench
            svg_content += f"""
    <!-- Deep Sea Trench & Fiber Cable -->
    <path d="M 100 850 Q 500 780 960 820 T 1820 750" fill="none" stroke="{p['accent_teal']}" stroke-width="8" stroke-linecap="round" />
    <path d="M 105 852 Q 502 782 962 822 T 1825 752" fill="none" stroke="#ffffff" stroke-width="3" stroke-linecap="round" opacity="0.8" />
    
    <!-- Optical Glass Core Detail -->
    <circle cx="960" cy="540" r="180" fill="#111827" stroke="{p['line_ink']}" stroke-width="4" />
    <circle cx="960" cy="540" r="176" fill="none" stroke="{p['accent_amber']}" stroke-width="2" stroke-dasharray="12 6" />
    <circle cx="960" cy="540" r="70" fill="url(#laser-glow)" />
    
    <!-- Light pulses -->
    <circle cx="820" cy="540" r="12" fill="{p['accent_teal']}" />
    <circle cx="1100" cy="540" r="12" fill="{p['accent_amber']}" />
    
    <!-- Labels -->
    <text x="960" y="780" text-anchor="middle" fill="{p['line_ink']}" font-family="monospace" font-size="24" letter-spacing="4">OPTICAL CARRIER SUBSEA CORE: 99.2% TRAFFIC</text>
"""
        elif act == 2:
            # Smartphone & Cellular Signaling Storm
            svg_content += f"""
    <!-- Smartphone Frame -->
    <rect x="780" y="220" width="360" height="640" rx="36" fill="#1e293b" stroke="{p['line_ink']}" stroke-width="5" />
    <rect x="804" y="270" width="312" height="520" rx="12" fill="#0f172a" />
    <line x1="910" y1="245" x2="1010" y2="245" stroke="{p['line_ink']}" stroke-width="4" stroke-linecap="round" />
    
    <!-- Frantic Cellular Wave Rings -->
    <circle cx="960" cy="530" r="90" fill="none" stroke="{p['accent_red']}" stroke-width="4" opacity="0.9" />
    <circle cx="960" cy="530" r="160" fill="none" stroke="{p['accent_red']}" stroke-width="3" stroke-dasharray="8 8" opacity="0.7" />
    <circle cx="960" cy="530" r="240" fill="none" stroke="{p['accent_red']}" stroke-width="2" opacity="0.4" />
    
    <!-- Cell Tower Icon -->
    <path d="M 400 800 L 480 350 L 560 800 Z" fill="none" stroke="{p['line_ink']}" stroke-width="4" />
    <line x1="440" y1="500" x2="520" y2="500" stroke="{p['line_ink']}" stroke-width="3" />
    <line x1="420" y1="650" x2="540" y2="650" stroke="{p['line_ink']}" stroke-width="3" />
    
    <!-- Error Text -->
    <text x="960" y="540" text-anchor="middle" fill="{p['accent_red']}" font-family="sans-serif" font-weight="bold" font-size="32">NO SERVICE</text>
    <text x="960" y="585" text-anchor="middle" fill="{p['line_ink']}" font-family="monospace" font-size="18">IEEE 1588 PTP SYNC LOST</text>
"""
        elif act == 3:
            # Point of Sale & Frozen Cash Register
            svg_content += f"""
    <!-- POS Terminal Unit -->
    <path d="M 720 300 L 1200 300 L 1280 780 L 640 780 Z" fill="#1e293b" stroke="{p['line_ink']}" stroke-width="5" />
    <rect x="760" y="340" width="400" height="240" rx="10" fill="#030712" stroke="{p['line_ink']}" stroke-width="3" />
    
    <!-- Terminal Screen Display -->
    <rect x="790" y="370" width="340" height="180" fill="#450a0a" rx="6" />
    <text x="960" y="450" text-anchor="middle" fill="{p['accent_red']}" font-family="sans-serif" font-weight="900" font-size="44" letter-spacing="4">TIMEOUT</text>
    <text x="960" y="500" text-anchor="middle" fill="#fca5a5" font-family="monospace" font-size="20">FEDWIRE GATEWAY OFFLINE</text>
    
    <!-- Keypad buttons -->
    <circle cx="820" cy="650" r="22" fill="#334155" />
    <circle cx="910" cy="650" r="22" fill="#334155" />
    <circle cx="1000" cy="650" r="22" fill="#334155" />
    <circle cx="1090" cy="650" r="22" fill="#334155" />
    
    <!-- Frozen Card Handshake -->
    <rect x="1100" y="440" width="220" height="140" rx="12" fill="{p['accent_amber']}" stroke="{p['line_ink']}" stroke-width="3" transform="rotate(-15 1100 440)" />
"""
        elif act == 4:
            # Industrial Logistics Warehouse & Container Crane
            svg_content += f"""
    <!-- Warehouse Shelving Matrix -->
    <g stroke="{p['line_ink']}" stroke-width="3" opacity="0.6">
      <line x1="200" y1="200" x2="200" y2="850" />
      <line x1="450" y1="200" x2="450" y2="850" />
      <line x1="200" y1="350" x2="450" y2="350" />
      <line x1="200" y1="520" x2="450" y2="520" />
      <line x1="200" y1="690" x2="450" y2="690" />
    </g>
    
    <!-- Frozen Automated Guided Vehicle (Robot) -->
    <rect x="800" y="680" width="320" height="140" rx="20" fill="#c2410c" stroke="{p['line_ink']}" stroke-width="4" />
    <circle cx="850" cy="820" r="30" fill="#0f172a" stroke="{p['line_ink']}" stroke-width="3" />
    <circle cx="1070" cy="820" r="30" fill="#0f172a" stroke="{p['line_ink']}" stroke-width="3" />
    <path d="M 960 620 L 960 680" stroke="{p['accent_amber']}" stroke-width="6" stroke-linecap="round" />
    <circle cx="960" cy="610" r="16" fill="{p['accent_red']}" />
    
    <!-- Frozen Cargo Crane Arm -->
    <path d="M 1300 200 L 1750 350 L 1750 500" fill="none" stroke="{p['line_ink']}" stroke-width="6" />
    <line x1="1550" y1="280" x2="1550" y2="600" stroke="{p['accent_amber']}" stroke-width="4" stroke-dasharray="10 10" />
    <rect x="1460" y="600" width="180" height="100" fill="#0369a1" stroke="{p['line_ink']}" stroke-width="4" />
    <text x="1550" y="660" text-anchor="middle" fill="#ffffff" font-family="monospace" font-size="20">MANIFEST UNKNOWN</text>
"""
        elif act == 5:
            # Electrical Grid SCADA & Substation Breakers
            svg_content += f"""
    <!-- High Voltage Transmission Tower -->
    <path d="M 880 200 L 1040 200 L 1120 880 L 800 880 Z" fill="none" stroke="{p['line_ink']}" stroke-width="5" />
    <line x1="720" y1="360" x2="1200" y2="360" stroke="{p['line_ink']}" stroke-width="5" />
    <line x1="760" y1="520" x2="1160" y2="520" stroke="{p['line_ink']}" stroke-width="5" />
    
    <!-- Transformer Arc Spark -->
    <circle cx="960" cy="620" r="140" fill="#1e1b4b" stroke="{p['accent_amber']}" stroke-width="4" />
    <path d="M 960 520 L 980 580 L 940 620 L 990 710" fill="none" stroke="{p['accent_gold']}" stroke-width="8" stroke-linecap="round" />
    
    <!-- SCADA Dial Gauge -->
    <circle cx="450" cy="600" r="100" fill="#0f172a" stroke="{p['line_ink']}" stroke-width="4" />
    <line x1="450" y1="600" x2="520" y2="540" stroke="{p['accent_red']}" stroke-width="6" stroke-linecap="round" />
    <text x="450" y="740" text-anchor="middle" fill="{p['accent_red']}" font-family="monospace" font-size="22">58.4 Hz [TRIP]</text>
"""
        elif act == 6:
            # Analog Renaissance & AM Radio Broadcast
            svg_content += f"""
    <!-- Cozy Vintage Transistor Radio -->
    <rect x="680" y="400" width="560" height="360" rx="30" fill="#78350f" stroke="{p['line_ink']}" stroke-width="5" />
    <rect x="710" y="430" width="500" height="300" rx="20" fill="#451a03" />
    
    <!-- Radio Speaker Grille -->
    <circle cx="850" cy="580" r="90" fill="#1c1917" stroke="{p['accent_amber']}" stroke-width="3" />
    <circle cx="850" cy="580" r="60" fill="#292524" />
    <circle cx="850" cy="580" r="30" fill="{p['accent_amber']}" />
    
    <!-- Glowing Tuning Needle -->
    <rect x="990" y="480" width="180" height="80" rx="8" fill="#fef3c7" stroke="{p['line_ink']}" stroke-width="2" />
    <line x1="1070" y1="480" x2="1070" y2="560" stroke="{p['accent_red']}" stroke-width="5" />
    <text x="1080" y="530" fill="#1e293b" font-family="monospace" font-weight="bold" font-size="20">880 kHz</text>
    
    <!-- Expanding Analog Radiance Waves -->
    <path d="M 1300 500 Q 1450 580 1300 660" fill="none" stroke="{p['accent_amber']}" stroke-width="4" stroke-linecap="round" />
    <path d="M 1360 440 Q 1550 580 1360 720" fill="none" stroke="{p['accent_amber']}" stroke-width="3" stroke-linecap="round" opacity="0.6" />
"""
        elif act == 7:
            # Thundering Herd & Reconnection Surge
            svg_content += f"""
    <!-- Massive Server Blade Array -->
    <g fill="#0f172a" stroke="{p['line_ink']}" stroke-width="3">
      <rect x="400" y="240" width="1120" height="120" rx="8" />
      <rect x="400" y="380" width="1120" height="120" rx="8" />
      <rect x="400" y="520" width="1120" height="120" rx="8" />
      <rect x="400" y="660" width="1120" height="120" rx="8" />
    </g>
    
    <!-- Blinking Server LEDs -->
    <circle cx="460" cy="300" r="10" fill="{p['accent_teal']}" />
    <circle cx="500" cy="300" r="10" fill="{p['accent_amber']}" />
    <circle cx="460" cy="440" r="10" fill="{p['accent_teal']}" />
    <circle cx="500" cy="440" r="10" fill="{p['accent_red']}" />
    
    <!-- The Packet Surge Flow -->
    <path d="M 100 900 Q 960 400 1820 900" fill="none" stroke="{p['accent_teal']}" stroke-width="12" stroke-linecap="round" opacity="0.7" />
    <text x="960" y="780" text-anchor="middle" fill="{p['accent_teal']}" font-family="monospace" font-weight="bold" font-size="34">RETRY STORM: 100 BILLION QUEUED REQS</text>
"""
        else:
            # The Final Illuminated Fiber in Human Hand
            svg_content += f"""
    <!-- The Investigator Silhouette -->
    <g stroke="{p['line_ink']}" stroke-width="4" fill="none">
      <!-- Head and Trench Collar -->
      <circle cx="960" cy="380" r="60" fill="#1e293b" />
      <path d="M 880 480 Q 960 440 1040 480 L 1080 820 L 840 820 Z" fill="#0f172a" />
      <!-- Hands cradling glowing strand -->
      <path d="M 860 620 Q 960 660 1060 620" stroke-width="6" stroke-linecap="round" />
    </g>
    
    <!-- Single Glowing Filament -->
    <line x1="400" y1="620" x2="1520" y2="620" stroke="{p['accent_amber']}" stroke-width="6" stroke-linecap="round" />
    <line x1="880" y1="620" x2="1040" y2="620" stroke="#ffffff" stroke-width="10" stroke-linecap="round" />
    <circle cx="960" cy="620" r="28" fill="url(#laser-glow)" />
    
    <!-- Documentary Sign-off -->
    <text x="960" y="900" text-anchor="middle" fill="{p['line_ink']}" font-family="sans-serif" font-weight="bold" font-size="36" letter-spacing="6">THE HIDDEN SYSTEMS</text>
    <text x="960" y="945" text-anchor="middle" fill="{p['accent_amber']}" font-family="monospace" font-size="20">THE INVISIBLE MACHINE OF CIVILIZATION</text>
"""

        # Scene watermark and Act label
        svg_content += f"""
  </g>

  <!-- UI Metadata Bar -->
  <rect x="40" y="40" width="380" height="48" rx="8" fill="#0f172a" opacity="0.85" stroke="#334155" stroke-width="1" />
  <text x="60" y="72" fill="{p['accent_amber']}" font-family="monospace" font-weight="bold" font-size="18">SCENE {scene.scene_id:02d} / 40</text>
  <text x="210" y="72" fill="{p['line_ink']}" font-family="sans-serif" font-size="16">ACT {scene.act_number}: {scene.transitions.upper()}</text>
</svg>"""

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(svg_content, encoding="utf-8")

        # Also render companion 1080p PNG for lossless FFmpeg animation
        png_path = output_path.with_suffix(".png")
        IllustrationAgent.generate_scene_png(scene, png_path)

        return str(output_path)

    @staticmethod
    def generate_scene_png(scene: StoryboardScene, output_png: Path) -> str:
        """
        Renders a high-resolution 1920x1080 hand-drawn editorial illustration
        matching the signature 'The Hidden Systems' visual identity.
        """
        from PIL import Image, ImageDraw, ImageFont
        w, h = 1920, 1080
        p = PALETTE

        # Base background
        img = Image.new("RGB", (w, h), color=p["background_deep"])
        draw = ImageDraw.Draw(img)

        # Technical background grid lines
        for x in range(0, w, 240):
            draw.line([(x, 0), (x, h)], fill="#151C28", width=1)
        for y in range(0, h, 180):
            draw.line([(0, y), (w, y)], fill="#151C28", width=1)

        # Outer editorial vignette border
        draw.rectangle([60, 60, w - 60, h - 60], outline="#1E293B", width=2)

        act = scene.act_number
        if act == 1:
            # Undersea Fiber Cable & Abyssal Glow
            draw.line([(100, 850), (960, 820), (1820, 750)], fill=p["accent_teal"], width=10)
            draw.line([(105, 852), (962, 822), (1825, 752)], fill="#FFFFFF", width=3)
            # Glass Core
            draw.ellipse([800, 380, 1120, 700], fill="#111827", outline=p["line_ink"], width=5)
            draw.ellipse([900, 480, 1020, 600], fill=p["accent_teal"], outline="#FFFFFF", width=4)
            draw.ellipse([930, 510, 990, 570], fill="#FFFFFF")
            # Signal pulses
            draw.ellipse([640, 530, 670, 560], fill=p["accent_amber"])
            draw.ellipse([1250, 530, 1280, 560], fill=p["accent_teal"])

        elif act == 2:
            # Smartphone & Red Signaling Waves
            draw.rectangle([800, 240, 1120, 840], fill="#1E293B", outline=p["line_ink"], width=6)
            draw.rectangle([830, 290, 1090, 770], fill="#0F172A", outline="#334155", width=2)
            # Red wave pulses
            draw.arc([760, 360, 1160, 760], start=0, end=360, fill=p["accent_red"], width=4)
            draw.arc([680, 280, 1240, 840], start=0, end=360, fill=p["accent_red"], width=3)
            draw.arc([600, 200, 1320, 920], start=0, end=360, fill="#7F1D1D", width=2)
            # Tower
            draw.line([(380, 840), (460, 380), (540, 840)], fill=p["line_ink"], width=5)
            draw.line([(420, 550), (500, 550)], fill=p["line_ink"], width=4)
            draw.line([(400, 700), (520, 700)], fill=p["line_ink"], width=4)

        elif act == 3:
            # Point of Sale & Frozen Terminal
            draw.polygon([(720, 320), (1200, 320), (1280, 800), (640, 800)], fill="#1E293B", outline=p["line_ink"])
            draw.rectangle([760, 360, 1160, 580], fill="#450A0A", outline=p["accent_red"], width=4)
            # Keypad
            for bx in [800, 900, 1000, 1100]:
                for by in [640, 720]:
                    draw.ellipse([bx - 20, by - 20, bx + 20, by + 20], fill="#334155", outline=p["line_ink"], width=2)

        elif act == 4:
            # Automated Warehouse & Robotic Carrier
            for rx in [300, 500, 700]:
                draw.line([(rx, 200), (rx, 800)], fill="#334155", width=4)
                draw.line([(rx, 350), (rx + 200, 350)], fill="#334155", width=3)
                draw.line([(rx, 550), (rx + 200, 550)], fill="#334155", width=3)
            # Robot unit
            draw.rounded_rectangle([800, 680, 1120, 820], radius=16, fill="#C2410C", outline=p["line_ink"], width=5)
            draw.ellipse([830, 800, 890, 860], fill="#0F172A", outline=p["line_ink"], width=4)
            draw.ellipse([1030, 800, 1090, 860], fill="#0F172A", outline=p["line_ink"], width=4)

        elif act == 5:
            # Substation & High-Voltage Flash
            draw.line([(880, 200), (1040, 200), (1120, 880), (800, 880), (880, 200)], fill=p["line_ink"], width=6)
            draw.line([(720, 380), (1200, 380)], fill=p["line_ink"], width=6)
            draw.line([(760, 560), (1160, 560)], fill=p["line_ink"], width=6)
            # Spark core
            draw.ellipse([840, 500, 1080, 740], fill="#1E1B4B", outline=p["accent_amber"], width=5)
            draw.line([(960, 520), (980, 580), (940, 620), (990, 710)], fill=p["accent_gold"], width=10)

        elif act == 6:
            # Transistor Radio & Warm Waves
            draw.rounded_rectangle([680, 400, 1240, 760], radius=24, fill="#78350F", outline=p["line_ink"], width=6)
            draw.rounded_rectangle([710, 430, 1210, 730], radius=16, fill="#451A03")
            draw.ellipse([750, 480, 930, 660], fill="#1C1917", outline=p["accent_amber"], width=4)
            draw.rectangle([980, 480, 1160, 580], fill="#FEF3C7", outline=p["line_ink"], width=3)
            draw.line([(1070, 480), (1070, 580)], fill=p["accent_red"], width=6)

        elif act == 7:
            # Server Array & Packet Surge
            for sy in [240, 380, 520, 660]:
                draw.rounded_rectangle([400, sy, 1520, sy + 110], radius=10, fill="#0F172A", outline=p["line_ink"], width=4)
                for led in [450, 500, 550]:
                    draw.ellipse([led, sy + 45, led + 20, sy + 65], fill=p["accent_teal"])
            # Surge arc
            draw.arc([100, 400, 1820, 1000], start=180, end=0, fill=p["accent_teal"], width=12)

        else:
            # Final Hand and Glowing Fiber Filament
            draw.ellipse([900, 320, 1020, 440], fill="#1E293B", outline=p["line_ink"], width=4)
            draw.polygon([(840, 450), (1080, 450), (1120, 800), (800, 800)], fill="#0F172A", outline=p["line_ink"])
            draw.line([(400, 620), (1520, 620)], fill=p["accent_amber"], width=8)
            draw.ellipse([920, 580, 1000, 660], fill="#FFFFFF", outline=p["accent_amber"], width=6)

        # Header Badge
        draw.rounded_rectangle([80, 70, 480, 130], radius=8, fill="#0F172A", outline="#334155", width=2)
        # Text label (default fallback font)
        title_str = f"THE HIDDEN SYSTEMS  |  SCENE {scene.scene_id:02d} / 40  |  ACT {act}"
        draw.text((100, 92), title_str, fill=p["accent_amber"])

        output_png.parent.mkdir(parents=True, exist_ok=True)
        img.save(str(output_png), "PNG")
        return str(output_png)
