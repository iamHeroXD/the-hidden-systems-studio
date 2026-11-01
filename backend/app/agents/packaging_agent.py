import subprocess
from pathlib import Path
from typing import List, Dict, Any, Tuple
from backend.app.models.schemas import ThumbnailConcept, VideoMetadata, ScriptDocument
from backend.app.agents.visual_agent import PALETTE

class PackagingAgent:
    @staticmethod
    def generate_thumbnails(topic_title: str, output_dir: Path) -> List[ThumbnailConcept]:
        """
        Generates 3 distinct, high-impact 1280x720 editorial hand-drawn thumbnails
        with high contrast, clear focal points, and YouTube CTR optimization.
        """
        output_dir.mkdir(parents=True, exist_ok=True)
        concepts: List[ThumbnailConcept] = []
        p = PALETTE

        # Concept 1: The Severed Fiber & Dark Earth
        svg_c1 = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720" width="1280" height="720">
  <defs>
    <radialGradient id="glow1" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="{p['accent_amber']}" stop-opacity="0.9" />
      <stop offset="100%" stop-color="{p['background_deep']}" stop-opacity="0" />
    </radialGradient>
  </defs>
  <rect width="1280" height="720" fill="{p['background_deep']}" />
  <circle cx="640" cy="360" r="320" fill="url(#glow1)" />
  
  <!-- Massive Severed Glowing Cable -->
  <path d="M 100 480 Q 450 360 580 360" fill="none" stroke="{p['accent_teal']}" stroke-width="24" stroke-linecap="round" />
  <path d="M 700 360 Q 830 360 1180 480" fill="none" stroke="{p['accent_red']}" stroke-width="24" stroke-linecap="round" />
  
  <!-- Sparking core -->
  <circle cx="580" cy="360" r="36" fill="#ffffff" />
  <circle cx="700" cy="360" r="36" fill="{p['accent_amber']}" />
  
  <!-- High Impact Typography -->
  <rect x="120" y="80" width="600" height="110" rx="12" fill="#0f172a" stroke="{p['accent_amber']}" stroke-width="4" />
  <text x="420" y="155" text-anchor="middle" fill="#ffffff" font-family="sans-serif" font-weight="900" font-size="64" letter-spacing="4">24 HOURS DARK</text>
</svg>"""

        # Concept 2: The Silent Smartphone & World Grid
        svg_c2 = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720" width="1280" height="720">
  <rect width="1280" height="720" fill="#090d16" />
  <circle cx="640" cy="360" r="280" fill="none" stroke="{p['accent_amber']}" stroke-width="3" stroke-dasharray="12 12" />
  <circle cx="640" cy="360" r="200" fill="none" stroke="#334155" stroke-width="2" />
  
  <!-- Giant Glowing Warning Icon -->
  <path d="M 640 180 L 760 380 L 520 380 Z" fill="{p['accent_red']}" stroke="#ffffff" stroke-width="8" />
  <rect x="632" y="240" width="16" height="70" rx="8" fill="#ffffff" />
  <circle cx="640" cy="340" r="10" fill="#ffffff" />
  
  <!-- Punchy Title Badge -->
  <rect x="240" y="460" width="800" height="150" rx="20" fill="#030712" stroke="{p['line_ink']}" stroke-width="6" />
  <text x="640" y="565" text-anchor="middle" fill="{p['accent_amber']}" font-family="sans-serif" font-weight="900" font-size="78">THE DAY IT STOPS</text>
</svg>"""

        # Concept 3: The Hand and the Machine
        svg_c3 = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720" width="1280" height="720">
  <rect width="1280" height="720" fill="#050811" />
  <path d="M 0 540 Q 640 280 1280 540" fill="none" stroke="{p['accent_teal']}" stroke-width="16" />
  
  <!-- Human Hand Silhouette reaching toward dying light -->
  <circle cx="640" cy="360" r="140" fill="#1e293b" stroke="{p['accent_gold']}" stroke-width="6" />
  <circle cx="640" cy="360" r="60" fill="{p['accent_gold']}" />
  
  <rect x="340" y="80" width="600" height="110" rx="14" fill="{p['accent_amber']}" />
  <text x="640" y="155" text-anchor="middle" fill="#000000" font-family="sans-serif" font-weight="900" font-size="64" letter-spacing="2">ZERO PACKETS</text>
</svg>"""

        thumb_svgs = [
            ("thumbnail_1", "The Severed Subsea Core", "High-voltage optical line snapped on abyssal floor", svg_c1),
            ("thumbnail_2", "The Silent Signal", "Global communication blackout warning beacon", svg_c2),
            ("thumbnail_3", "Zero Packets", "Minimalist hand reaching toward dying network matrix", svg_c3)
        ]

        for idx, (fname, focal, desc, svg_code) in enumerate(thumb_svgs, start=1):
            svg_file = output_dir / f"{fname}.svg"
            png_file = output_dir / f"{fname}.png"
            svg_file.write_text(svg_code, encoding="utf-8")

            # Render 1280x720 thumbnail PNG directly via Pillow
            from PIL import Image, ImageDraw
            t_img = Image.new("RGB", (1280, 720), color="#080B11")
            t_draw = ImageDraw.Draw(t_img)
            
            # Draw distinctive thumbnail art
            if idx == 1:
                t_draw.line([(100, 480), (580, 360)], fill=p["accent_teal"], width=20)
                t_draw.line([(700, 360), (1180, 480)], fill=p["accent_red"], width=20)
                t_draw.ellipse([540, 320, 620, 400], fill="#FFFFFF")
                t_draw.ellipse([660, 320, 740, 400], fill=p["accent_amber"])
                short_t = topic_title[:32].upper()
                t_draw.rounded_rectangle([180, 80, 1100, 200], radius=16, fill="#0F172A", outline=p["accent_amber"], width=5)
                t_draw.text((240, 115), f"THE HIDDEN SYSTEMS: {short_t}", fill="#FFFFFF")
            elif idx == 2:
                short_t = topic_title[:28].upper()
                t_draw.ellipse([360, 100, 920, 660], outline=p["accent_amber"], width=4)
                t_draw.polygon([(640, 180), (760, 380), (520, 380)], fill=p["accent_red"], outline="#FFFFFF")
                t_draw.rounded_rectangle([200, 460, 1080, 620], radius=20, fill="#030712", outline=p["line_ink"], width=6)
                t_draw.text((320, 520), f"EXPOSED: {short_t}", fill=p["accent_amber"])
            else:
                short_t = topic_title[:28].upper()
                t_draw.line([(0, 540), (1280, 540)], fill=p["accent_teal"], width=12)
                t_draw.ellipse([540, 260, 740, 460], fill="#1E293B", outline=p["accent_gold"], width=6)
                t_draw.rounded_rectangle([280, 80, 1000, 200], radius=16, fill=p["accent_amber"])
                t_draw.text((360, 120), f"CLASSIFIED: {short_t}", fill="#000000")

            t_img.save(str(png_file), "PNG")

            concepts.append(ThumbnailConcept(
                id=idx,
                title=f"Concept {idx}: {focal}",
                focal_subject=focal,
                visual_description=desc,
                contrast_color="#F59E0B",
                file_path=str(png_file)
            ))

        return concepts

    @staticmethod
    def generate_metadata(script: ScriptDocument) -> VideoMetadata:
        title = script.title
        title_options = [
            f"{title}",
            f"The Hidden Reality of {title}: Explained",
            f"Why Nobody Talks About {title} (Until Now)"
        ]

        chapters = []
        cum_sec = 0
        for act in script.acts:
            m = int(cum_sec // 60)
            s = int(cum_sec % 60)
            chapters.append({"time": f"{m:02d}:{s:02d}", "title": act.title})
            cum_sec += int(act.word_count / 2.4)

        description = (
            f"Welcome to THE HIDDEN SYSTEMS.\n\n"
            f"In this documentary, we investigate: {title}.\n\n"
            f"{script.full_text[:400]}...\n\n"
            "TIMESTAMPS:\n" +
            "\n".join([f"{c['time']} - {c['title']}" for c in chapters]) +
            "\n\nSOURCES & VERIFIED RESEARCH:\n" +
            "\n".join([f"- {cite}" for act in script.acts for cite in act.factual_citations[:2]]) +
            "\n\n#TheHiddenSystems #Technology #ComputerScience #Engineering #Documentary"
        )

        clean_slug = title.lower().replace("what if ", "").replace("the ", "")
        tags = [
            "the hidden systems", title.lower(), clean_slug,
            "computer science documentary", "hidden infrastructure",
            "technology explainer", "2d animated documentary", "engineering explained"
        ]

        hashtags = ["#TheHiddenSystems", "#Technology", "#ComputerScience", "#Documentary"]
        pinned_comment = (
            f"What was the most surprising revelation in this breakdown of {title}? "
            "Drop your thoughts below."
        )

        return VideoMetadata(
            title_options=title_options,
            final_title=title_options[0],
            description=description,
            chapters=chapters,
            tags=tags,
            hashtags=hashtags,
            pinned_comment=pinned_comment,
            source_references=[cite for act in script.acts for cite in act.factual_citations]
        )
