from pathlib import Path
from typing import List, Dict, Any
from backend.app.models.schemas import StoryboardScene

class SubtitlesAgent:
    @staticmethod
    def format_timestamp_srt(seconds: float) -> str:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds - int(seconds)) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

    @staticmethod
    def format_timestamp_vtt(seconds: float) -> str:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds - int(seconds)) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millis:03d}"

    @staticmethod
    def generate_subtitles(scenes: List[StoryboardScene], output_dir: Path) -> Dict[str, str]:
        """
        Builds properly synchronized SRT and VTT subtitle files based on scene narration chunks.
        """
        output_dir.mkdir(parents=True, exist_ok=True)
        srt_path = output_dir / "captions.srt"
        vtt_path = output_dir / "captions.vtt"

        srt_lines = []
        vtt_lines = ["WEBVTT\n"]

        current_time = 0.0
        caption_idx = 1

        for scene in scenes:
            start_time = current_time
            end_time = current_time + scene.duration_sec
            
            # Break narration chunk into readable 8-12 word subtitle slices
            words = scene.narration_chunk.split()
            sub_chunk_size = 10
            for i in range(0, len(words), sub_chunk_size):
                slice_words = " ".join(words[i:i + sub_chunk_size])
                slice_dur = scene.duration_sec * (len(slice_words.split()) / max(1, len(words)))
                sub_start = start_time
                sub_end = min(end_time, sub_start + slice_dur)

                start_srt = SubtitlesAgent.format_timestamp_srt(sub_start)
                end_srt = SubtitlesAgent.format_timestamp_srt(sub_end)
                start_vtt = SubtitlesAgent.format_timestamp_vtt(sub_start)
                end_vtt = SubtitlesAgent.format_timestamp_vtt(sub_end)

                # SRT entry
                srt_lines.append(f"{caption_idx}\n{start_srt} --> {end_srt}\n{slice_words}\n")

                # VTT entry
                vtt_lines.append(f"{caption_idx}\n{start_vtt} --> {end_vtt}\n{slice_words}\n")

                caption_idx += 1
                start_time = sub_end

            current_time = end_time

        srt_content = "\n".join(srt_lines)
        vtt_content = "\n".join(vtt_lines)

        srt_path.write_text(srt_content, encoding="utf-8")
        vtt_path.write_text(vtt_content, encoding="utf-8")

        return {
            "srt": str(srt_path),
            "vtt": str(vtt_path)
        }
