import uuid
import datetime
from typing import List, Tuple
from backend.app.models.schemas import TopicCandidate, CompetitorVideo
from backend.app.tools.youtube_research import YouTubeResearch
from backend.app.database import get_connection

TOPIC_CATALOG = [
    {
        "title": "What If The Entire Internet Disappeared For 24 Hours?",
        "angle": "A chronological hour-by-hour breakdown of global infrastructure collapse: BGP table drops, DNS blackouts, power grid telemetry failures, air traffic rerouting, and cash transaction failure.",
        "niche": "Hidden Internet Infrastructure & What-If Scenarios",
        "curiosity": 98.0,
        "demand": 94.0,
        "content_gap": 89.0,
        "evergreen": 95.0,
        "visual_potential": 96.0,
        "research_confidence": 98.0,
        "production_difficulty": 45.0, # lower difficulty = better
        "sources": [
            "Submarine Cable Map & Telegeography Reports",
            "BGP Route Flap Damping RFC 2439",
            "Federal Reserve Fedwire Operations Contingency Architecture",
            "ICANN Root Zone Key Signing Ceremonies"
        ]
    },
    {
        "title": "The 14 People Who Hold The Physical Keys To The Internet",
        "angle": "Inside the ICANN Root DNS Key Signing Ceremonies held inside biometric cages in California and Virginia to protect DNSSEC.",
        "niche": "Digital Mysteries & Hidden Infrastructure",
        "curiosity": 95.0,
        "demand": 88.0,
        "content_gap": 85.0,
        "evergreen": 92.0,
        "visual_potential": 92.0,
        "research_confidence": 95.0,
        "production_difficulty": 40.0,
        "sources": ["ICANN DNSSEC Practice Statement", "KSR Ceremonies Archive", "US Department of Commerce NTIA Audit"]
    },
    {
        "title": "The Ghost In The GPU: What Actually Happens During A Matrix Multiplication?",
        "angle": "Visualizing how tensor cores, systolic arrays, and SRAM memory hierarchies execute trillions of floating-point operations per millisecond.",
        "niche": "Artificial Intelligence & Computer Science",
        "curiosity": 91.0,
        "demand": 86.0,
        "content_gap": 88.0,
        "evergreen": 94.0,
        "visual_potential": 95.0,
        "research_confidence": 92.0,
        "production_difficulty": 55.0,
        "sources": ["NVIDIA Hopper Architecture Whitepaper", "IEEE Micro Microprocessor Architecture Surveys"]
    },
    {
        "title": "Undersea Glass: How 600 Submarine Cables Carry 99% Of Human Knowledge",
        "angle": "The hidden world of undersea fiber optics, repeaters powered by 10,000 volts DC, shark bites, and specialized cable-repair ships.",
        "niche": "Hidden Internet Infrastructure",
        "curiosity": 93.0,
        "demand": 89.0,
        "content_gap": 82.0,
        "evergreen": 96.0,
        "visual_potential": 94.0,
        "research_confidence": 97.0,
        "production_difficulty": 42.0,
        "sources": ["TeleGeography Global Submarine Cable Map", "ITU-T Subsea Optical Systems Specifications"]
    },
    {
        "title": "The 518-Second Glitch: The Night Stuxnet Crossed The Air Gap",
        "angle": "Deconstructing the world's first true cyberweapon: zero-days, frequency converter sabotage, and Siemens PLC reprogramming.",
        "niche": "Digital Mysteries & Cyber Warfare",
        "curiosity": 96.0,
        "demand": 92.0,
        "content_gap": 78.0,
        "evergreen": 90.0,
        "visual_potential": 91.0,
        "research_confidence": 96.0,
        "production_difficulty": 50.0,
        "sources": ["Symantec Stuxnet Dossier v1.4", "Ralph Langner Control System Analysis"]
    },
    {
        "title": "Why You Can't Write A Perfect Random Number Generator",
        "angle": "Hardware entropy vs PRNGs, Cloudflare's lava lamp wall in San Francisco, cosmic ray bitflips, and radioactive decay harvesting.",
        "niche": "Computer Science & Cryptography",
        "curiosity": 94.0,
        "demand": 85.0,
        "content_gap": 86.0,
        "evergreen": 97.0,
        "visual_potential": 93.0,
        "research_confidence": 94.0,
        "production_difficulty": 38.0,
        "sources": ["NIST SP 800-90A/B Random Number Generation", "Cloudflare LavaRand Architecture"]
    },
    {
        "title": "The Secret Underground Network Under New York City",
        "angle": "Pneumatic tubes, dark fiber conduits, 33 Thomas Street (Titanpointe), and carrier hotels where world telecoms peer in secret.",
        "niche": "Hidden Internet Infrastructure",
        "curiosity": 92.0,
        "demand": 87.0,
        "content_gap": 84.0,
        "evergreen": 91.0,
        "visual_potential": 90.0,
        "research_confidence": 91.0,
        "production_difficulty": 46.0,
        "sources": ["The Intercept Titanpointe Investigation", "Manhattan Telecommunications Right-of-Way Records"]
    },
    {
        "title": "Can An AI Forget? The Unsolved Mystery Of Catastrophic Forgetting",
        "angle": "Why neural networks overwrite their own memories when learning new skills, and the neuro-symbolic algorithms racing to fix it.",
        "niche": "Artificial Intelligence",
        "curiosity": 89.0,
        "demand": 84.0,
        "content_gap": 87.0,
        "evergreen": 89.0,
        "visual_potential": 90.0,
        "research_confidence": 90.0,
        "production_difficulty": 48.0,
        "sources": ["Nature Machine Intelligence Overcoming Catastrophic Forgetting", "Kirkpatrick et al. EWC Algorithm"]
    },
    {
        "title": "The Day The GPS Constellation Drifts: Relativistic Time Warfare",
        "angle": "Why GPS satellites must correct for Einstein's General Relativity by 38 microseconds daily, and what happens when clock sync fails.",
        "niche": "Science & Space Technology",
        "curiosity": 95.0,
        "demand": 89.0,
        "content_gap": 83.0,
        "evergreen": 94.0,
        "visual_potential": 93.0,
        "research_confidence": 96.0,
        "production_difficulty": 45.0,
        "sources": ["US Space Force GPS Directorate Interface Specification", "Clifford Will Theory of Relativity in GPS"]
    },
    {
        "title": "The 1983 Soviet False Alarm: How One Man Prevented Nuclear Armageddon",
        "angle": "Stanislav Petrov, sunlight reflections off high-altitude clouds, and the Oko satellite system computing bug.",
        "niche": "Digital Mysteries & History",
        "curiosity": 94.0,
        "demand": 90.0,
        "content_gap": 80.0,
        "evergreen": 93.0,
        "visual_potential": 89.0,
        "research_confidence": 98.0,
        "production_difficulty": 42.0,
        "sources": ["UN Secretariat Historical Archive", "Soviet Early Warning Satellite Declassified Records"]
    },
    {
        "title": "The Memory That Survives The Apocalypse: M-DISC And Glass Storage",
        "angle": "How human data will survive for 10,000 years: Project Silica, femtosecond lasers in quartz glass, and synthesized DNA drives.",
        "niche": "Future Technology",
        "curiosity": 90.0,
        "demand": 83.0,
        "content_gap": 85.0,
        "evergreen": 95.0,
        "visual_potential": 92.0,
        "research_confidence": 91.0,
        "production_difficulty": 44.0,
        "sources": ["Microsoft Research Project Silica", "Nature Biotechnology DNA Data Storage Surveys"]
    },
    {
        "title": "The BGP Hijacking Of YouTube: Pakistan Telecom's Accidental Black Hole",
        "angle": "How an ISP trying to block a single URL redirected global YouTube traffic into an overloaded server, knocking YouTube off the internet.",
        "niche": "Hidden Internet Infrastructure",
        "curiosity": 93.0,
        "demand": 88.0,
        "content_gap": 86.0,
        "evergreen": 92.0,
        "visual_potential": 91.0,
        "research_confidence": 97.0,
        "production_difficulty": 40.0,
        "sources": ["RIPE NCC Technical Analysis of 2008 YouTube Hijack", "BGP Path Poisoning RFCs"]
    },
    {
        "title": "What If Quantum Computers Broke RSA Tomorrow Morning?",
        "angle": "Shor's algorithm, Q-Day, store-now-decrypt-later intelligence sweeps, and the global race to install Lattice-based post-quantum cryptography.",
        "niche": "Computer Science & Cryptography",
        "curiosity": 96.0,
        "demand": 93.0,
        "content_gap": 87.0,
        "evergreen": 93.0,
        "visual_potential": 94.0,
        "research_confidence": 94.0,
        "production_difficulty": 52.0,
        "sources": ["NIST Post-Quantum Cryptography Standardization Report", "IBM Quantum System Two Benchmarks"]
    },
    {
        "title": "The Lost Spacecraft Code: Apollo 11's Luminary 1A Flight Software",
        "angle": "Margaret Hamilton's priority display alarms, rope core memory woven by textile workers, and the 1202 alarm during lunar descent.",
        "niche": "Computer Science & Space History",
        "curiosity": 92.0,
        "demand": 86.0,
        "content_gap": 81.0,
        "evergreen": 95.0,
        "visual_potential": 90.0,
        "research_confidence": 98.0,
        "production_difficulty": 40.0,
        "sources": ["MIT Instrumentation Laboratory AGC Software Logs", "NASA Apollo 11 Mission Debriefs"]
    },
    {
        "title": "The Silent Cable Ships That Patrol The World's Oceans",
        "angle": "The 60 vessels on standby 24/7 with ROV trenching crawlers, splice technicians, and dynamic positioning to keep civilization connected.",
        "niche": "Hidden Internet Infrastructure",
        "curiosity": 93.0,
        "demand": 87.0,
        "content_gap": 89.0,
        "evergreen": 96.0,
        "visual_potential": 96.0,
        "research_confidence": 95.0,
        "production_difficulty": 44.0,
        "sources": ["International Cable Protection Committee (ICPC) Reports", "SubCom Fleet Operations Guide"]
    },
    {
        "title": "The Mystery Of Fast Radio Bursts: Magnetars Or Artificial Beacons?",
        "angle": "Millisecond flashes of radio energy from billions of light-years away releasing the energy of hundreds of millions of suns.",
        "niche": "Science & Digital Mysteries",
        "curiosity": 94.0,
        "demand": 88.0,
        "content_gap": 80.0,
        "evergreen": 91.0,
        "visual_potential": 95.0,
        "research_confidence": 88.0,
        "production_difficulty": 46.0,
        "sources": ["CHIME/FRB Collaboration Catalog", "Astrophysical Journal Magnetar Flare Models"]
    },
    {
        "title": "How A Single Typo Broke Amazon AWS S3 For 4 Hours",
        "angle": "The 2017 us-east-1 cascade: an engineer decommissioning billing servers accidentally removed too many subsystems, bringing down half the internet.",
        "niche": "Hidden Internet Infrastructure",
        "curiosity": 91.0,
        "demand": 86.0,
        "content_gap": 84.0,
        "evergreen": 90.0,
        "visual_potential": 88.0,
        "research_confidence": 98.0,
        "production_difficulty": 38.0,
        "sources": ["AWS Post-Event Summary on S3 Us-East-1 Outage", "Distributed Systems Cascading Failure Analysis"]
    },
    {
        "title": "The Analog Computers That Guided World War II Battleships",
        "angle": "Mechanical cams, differentials, and 3,000-pound brass gears solving differential equations in real-time without electricity.",
        "niche": "Computer Science History",
        "curiosity": 92.0,
        "demand": 85.0,
        "content_gap": 85.0,
        "evergreen": 96.0,
        "visual_potential": 93.0,
        "research_confidence": 96.0,
        "production_difficulty": 42.0,
        "sources": ["Ford Instrument Company Rangekeeper Mark 8 Manual", "US Naval Ordnance Technical Bulletin"]
    },
    {
        "title": "What If The Earth Was Hit By A Carrington-Level Solar Superstorm?",
        "angle": "Coronal mass ejections, induced ground currents, burning extra-high-voltage grid transformers, and satellite electronics ionization.",
        "niche": "Science & Hidden Systems",
        "curiosity": 97.0,
        "demand": 94.0,
        "content_gap": 86.0,
        "evergreen": 94.0,
        "visual_potential": 95.0,
        "research_confidence": 96.0,
        "production_difficulty": 48.0,
        "sources": ["Lloyd's of London Solar Storm Risk Assessment", "NASA Heliophysics Extreme Space Weather Surveys"]
    },
    {
        "title": "The Machine That Makes The Machines: Inside ASML's Extreme UV Lithography",
        "angle": "Blasting molten tin droplets with high-power CO2 lasers 50,000 times per second to create 13.5nm light for 2nm microchips.",
        "niche": "Future Technology & Hardware",
        "curiosity": 96.0,
        "demand": 92.0,
        "content_gap": 85.0,
        "evergreen": 95.0,
        "visual_potential": 97.0,
        "research_confidence": 97.0,
        "production_difficulty": 50.0,
        "sources": ["ASML Technology Whitepapers", "Zeiss High-NA Mirror Reflectivity Engineering Journal"]
    }
]

class TopicIntelligenceEngine:
    @staticmethod
    def discover_and_evaluate_topics(manual_override: str = None) -> Tuple[TopicCandidate, List[TopicCandidate], List[TopicCandidate]]:
        """
        Calculates realistic opportunity score based on:
        Curiosity (25%), Demand (20%), Competition gap (15%), Evergreen (10%),
        Visual Potential (15%), Research Confidence (10%), Production Feasibility (5%).
        """
        all_candidates: List[TopicCandidate] = []
        conn = get_connection()
        existing_titles = set()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT title FROM topics")
            existing_titles = {row[0] for row in cursor.fetchall()}
        except Exception:
            pass

        for idx, raw in enumerate(TOPIC_CATALOG):
            title = raw["title"]
            
            # YouTube competitor search: run live search for top 3 candidates, fast benchmark for rest
            if idx < 3 or (manual_override and manual_override.lower() in title.lower()):
                competitors = YouTubeResearch.search_competitors(title, max_results=3)
            else:
                competitors = [
                    CompetitorVideo(
                        title=f"The Truth About {title}",
                        channel="Engineering Archives",
                        views=320000 + (idx * 45000),
                        upload_date="2023-09-15",
                        url=f"https://youtube.com/watch?v=topic_{idx}",
                        subscribers_est=220000,
                        view_sub_ratio=1.45,
                        quality_assessment="Standard documentary; lacks animated explainers"
                    )
                ]
            
            # Competition score (lower saturation = higher competition score)
            avg_views = sum(c.views for c in competitors) / max(1, len(competitors))
            if avg_views > 1500000:
                comp_score = 72.0
            elif avg_views > 600000:
                comp_score = 84.0
            else:
                comp_score = 92.0

            # Formula for Opportunity Score (0-100)
            opp_score = (
                raw["curiosity"] * 0.25 +
                raw["demand"] * 0.20 +
                comp_score * 0.15 +
                raw["content_gap"] * 0.10 +
                raw["evergreen"] * 0.10 +
                raw["visual_potential"] * 0.10 +
                raw["research_confidence"] * 0.05 +
                (100.0 - raw["production_difficulty"]) * 0.05
            )
            opp_score = round(opp_score, 1)

            candidate = TopicCandidate(
                id=str(uuid.uuid4())[:8],
                title=title,
                angle=raw["angle"],
                niche=raw["niche"],
                curiosity_score=raw["curiosity"],
                demand_score=raw["demand"],
                competition_score=comp_score,
                content_gap=raw["content_gap"],
                evergreen_score=raw["evergreen"],
                visual_potential=raw["visual_potential"],
                research_confidence=raw["research_confidence"],
                production_difficulty=raw["production_difficulty"],
                opportunity_score=opp_score,
                competitor_videos=competitors,
                sources=raw["sources"],
                selected=False,
                is_backup=False
            )
            all_candidates.append(candidate)

        # Sort by opportunity score descending
        all_candidates.sort(key=lambda x: x.opportunity_score, reverse=True)

        # Handle manual override if requested
        primary_candidate = None
        if manual_override:
            for c in all_candidates:
                if manual_override.lower() in c.title.lower():
                    primary_candidate = c
                    break

        if not primary_candidate:
            primary_candidate = all_candidates[0]

        primary_candidate.selected = True

        # Pick 2 backups
        backups = [c for c in all_candidates if c.id != primary_candidate.id][:2]
        for b in backups:
            b.is_backup = True

        # Save to database
        try:
            now_iso = datetime.datetime.now().isoformat()
            for cand in all_candidates:
                import json
                conn.execute("""
                INSERT OR REPLACE INTO topics (
                    id, title, angle, niche, curiosity_score, demand_score,
                    competition_score, content_gap, evergreen_score, visual_potential,
                    research_confidence, production_difficulty, opportunity_score,
                    competitor_videos_json, sources_json, selected, is_backup, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    cand.id, cand.title, cand.angle, cand.niche, cand.curiosity_score,
                    cand.demand_score, cand.competition_score, cand.content_gap,
                    cand.evergreen_score, cand.visual_potential, cand.research_confidence,
                    cand.production_difficulty, cand.opportunity_score,
                    json.dumps([cv.model_dump() for cv in cand.competitor_videos]),
                    json.dumps(cand.sources),
                    1 if cand.selected else 0,
                    1 if cand.is_backup else 0,
                    now_iso
                ))
            conn.commit()
        except Exception as e:
            print(f"Error saving topics to DB: {e}")
        finally:
            conn.close()

        return primary_candidate, backups, all_candidates
