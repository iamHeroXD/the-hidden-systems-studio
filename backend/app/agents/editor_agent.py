import os
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Tuple
from backend.app.config import settings

class EditorAgent:
    @staticmethod
    def generate_ambient_soundtrack(duration_sec: float, output_path: Path) -> Path:
        """
        Synthesizes a copyright-safe, atmospheric, mysterious documentary score
        using procedural FFmpeg audio filters (warm minor drones, subtle flanger).
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        # Complex audio filter: layered 110Hz (A2), 165Hz (E3), and 220Hz (A3) sine waves with lowpass filter
        cmd = [
            "ffmpeg", "-y",
            "-f", "lavfi",
            "-i", f"sine=frequency=110:duration={duration_sec}",
            "-f", "lavfi",
            "-i", f"sine=frequency=165:duration={duration_sec}",
            "-f", "lavfi",
            "-i", f"anoisesrc=d={duration_sec}:c=pink:r=44100:a=0.01",
            "-filter_complex",
            f"[0:a]volume=0.25[a0];[1:a]volume=0.15[a1];[2:a]lowpass=f=400,volume=0.08[a2];"
            f"[a0][a1][a2]amix=inputs=3:duration=first[mixed];"
            f"[mixed]flanger=delay=15:depth=4:regen=20:width=80:speed=0.2[flanged];"
            f"[flanged]afade=t=in:ss=0:d=2,afade=t=out:st={max(2.0, duration_sec - 2.0)}:d=2[out]",
            "-map", "[out]",
            "-c:a", "libmp3lame",
            "-b:a", "192k",
            str(output_path)
        ]
        subprocess.run(cmd, capture_output=True, timeout=120)
        return output_path

    @staticmethod
    def assemble_final_video(
        scene_video_paths: List[str],
        narration_audio_path: Path,
        subtitles_srt_path: Path,
        output_dir: Path
    ) -> Tuple[Path, Path]:
        """
        Stitches all scene videos, mixes narration with ambient background score,
        normalizes audio with EBU R128 loudnorm, and encodes final 1080p and preview 720p MP4.
        """
        output_dir.mkdir(parents=True, exist_ok=True)
        final_mp4 = output_dir / "final_1080p.mp4"
        preview_mp4 = output_dir / "preview_720p.mp4"

        # 1. Create scene concatenation manifest
        concat_list = output_dir / "scenes_concat.txt"
        with open(concat_list, "w", encoding="utf-8") as f:
            for p in scene_video_paths:
                clean_p = Path(p).resolve().as_posix()
                f.write(f"file '{clean_p}'\n")

        # 2. Concat raw scenes into video track
        raw_video = output_dir / "raw_video_stitched.mp4"
        cmd_concat = [
            "ffmpeg", "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", str(concat_list),
            "-c", "copy",
            str(raw_video)
        ]
        subprocess.run(cmd_concat, capture_output=True, timeout=180)

        # 3. Determine video duration using ffprobe
        dur_cmd = [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            str(raw_video)
        ]
        res = subprocess.run(dur_cmd, capture_output=True, text=True)
        duration = float(res.stdout.strip() or 180.0)

        # 4. Generate ambient music score matching exact duration
        bgm_path = output_dir / "ambient_score.mp3"
        EditorAgent.generate_ambient_soundtrack(duration, bgm_path)

        # 5. Mux Video + Voice (Loudnorm -16 LUFS) + BGM (-22dB ducking)
        cmd_final = [
            "ffmpeg", "-y",
            "-i", str(raw_video),
            "-i", str(narration_audio_path),
            "-i", str(bgm_path),
            "-filter_complex",
            # Voice loudnorm + ducked BGM
            "[1:a]loudnorm=I=-16:TP=-1.5:LRA=11[voice];"
            "[2:a]volume=0.15[bgm];"
            "[voice][bgm]amix=inputs=2:duration=first:dropout_transition=2[aout]",
            "-map", "0:v",
            "-map", "[aout]",
            "-c:v", "copy",
            "-c:a", "aac",
            "-b:a", "192k",
            "-shortest",
            str(final_mp4)
        ]
        
        proc = subprocess.run(cmd_final, capture_output=True, text=True, timeout=300)
        if proc.returncode != 0 or not final_mp4.exists():
            # If complex filter encountered issue with audio, fallback to direct audio copy
            cmd_fallback = [
                "ffmpeg", "-y",
                "-i", str(raw_video),
                "-i", str(narration_audio_path),
                "-c:v", "copy",
                "-c:a", "aac",
                "-shortest",
                str(final_mp4)
            ]
            subprocess.run(cmd_fallback, capture_output=True, timeout=120)

        # 6. Generate lightweight 720p preview
        cmd_prev = [
            "ffmpeg", "-y",
            "-i", str(final_mp4),
            "-vf", "scale=1280:720",
            "-c:v", "libx264",
            "-preset", "ultrafast",
            "-crf", "26",
            "-c:a", "copy",
            str(preview_mp4)
        ]
        subprocess.run(cmd_prev, capture_output=True, timeout=180)

        return final_mp4, preview_mp4
