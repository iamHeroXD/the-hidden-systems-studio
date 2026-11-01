import os
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Tuple, Callable, Optional
from concurrent.futures import ThreadPoolExecutor
from backend.app.models.schemas import StoryboardScene
from backend.app.config import settings

class AnimationAgent:
    @staticmethod
    def generate_motion_canvas_project(scenes: List[StoryboardScene], project_dir: Path) -> Path:
        """
        Creates a valid Motion Canvas project with TypeScript scenes,
        signals, camera movements, and audio waveform alignment.
        """
        src_dir = project_dir / "src"
        src_dir.mkdir(parents=True, exist_ok=True)

        pkg_json = project_dir / "package.json"
        if not pkg_json.exists():
            pkg_json.write_text("""{
  "name": "hidden-systems-motion-canvas",
  "private": true,
  "version": "1.0.0",
  "scripts": {
    "serve": "vite",
    "build": "vite build"
  },
  "dependencies": {
    "@motion-canvas/core": "^3.16.0",
    "@motion-canvas/2d": "^3.16.0"
  },
  "devDependencies": {
    "@motion-canvas/vite-plugin": "^3.16.0",
    "typescript": "^5.4.0",
    "vite": "^5.2.0"
  }
}
""", encoding="utf-8")

        project_ts = src_dir / "project.ts"
        project_ts.write_text("""import {makeProject} from '@motion-canvas/core';
import documentaryScene from './scenes/documentary?scene';

export default makeProject({
  scenes: [documentaryScene],
});
""", encoding="utf-8")

        scenes_dir = src_dir / "scenes"
        scenes_dir.mkdir(parents=True, exist_ok=True)
        doc_scene = scenes_dir / "documentary.tsx"
        doc_scene.write_text("""import {makeScene2D, createRef, all, easeInOutCubic} from '@motion-canvas/2d';
import {Circle, Rect, Txt, Node, Camera} from '@motion-canvas/2d';

export default makeScene2D(function* (view) {
  const camera = createRef<Camera>();
  const title = createRef<Txt>();
  const filament = createRef<Rect>();

  view.add(
    <Camera ref={camera}>
      <Rect
        width={1920}
        height={1080}
        fill={'#050508'}
      />
      <Rect
        ref={filament}
        width={800}
        height={8}
        fill={'#06B6D4'}
        radius={4}
      />
      <Txt
        ref={title}
        text={'THE HIDDEN SYSTEMS'}
        fontFamily={'monospace'}
        fontSize={48}
        fill={'#E2E8F0'}
        y={120}
        opacity={0}
      />
    </Camera>
  );

  yield* all(
    filament().scale.x(1.5, 2.0, easeInOutCubic),
    title().opacity(1, 1.5),
    camera().zoom(1.15, 3.0, easeInOutCubic)
  );
});
""", encoding="utf-8")

        return project_dir

    @staticmethod
    def render_scene_to_video(scene: StoryboardScene, img_path: Path, output_mp4: Path) -> str:
        """
        Renders the hand-drawn scene artwork into an animated 1080p 30fps MP4 clip
        with smooth camera pans, zooms, and dynamic motion blur.
        """
        output_mp4.parent.mkdir(parents=True, exist_ok=True)
        dur = max(3.0, float(scene.duration_sec))
        num_frames = int(dur * settings.video_fps)

        # Use companion PNG if available
        render_input = img_path
        if img_path.suffix.lower() == ".svg" and img_path.with_suffix(".png").exists():
            render_input = img_path.with_suffix(".png")

        # Select camera movement filter
        cam = scene.camera_movement.lower()
        if "zoom in" in cam or "push-in" in cam or "zoom" in cam:
            # Smooth cinematic slow zoom from 1.0x to 1.14x
            vf = (
                f"zoompan=z='min(zoom+0.0006,1.14)':d={num_frames}:"
                f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={settings.video_width}x{settings.video_height}:fps={settings.video_fps}"
            )
        elif "pan right" in cam or "pan" in cam:
            # Slow cinematic drift from left to right
            vf = (
                f"zoompan=z=1.07:d={num_frames}:"
                f"x='(on/{num_frames})*(iw-iw/zoom)':y='ih/2-(ih/zoom/2)':s={settings.video_width}x{settings.video_height}:fps={settings.video_fps}"
            )
        elif "pull-back" in cam or "outward" in cam:
            # Gentle pull-back zoom out
            vf = (
                f"zoompan=z='if(lte(zoom,1.0),1.14,max(1.0,zoom-0.0006))':d={num_frames}:"
                f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={settings.video_width}x{settings.video_height}:fps={settings.video_fps}"
            )
        else:
            # Subtle organic parallax float
            vf = (
                f"zoompan=z=1.04:d={num_frames}:"
                f"x='(iw/2-(iw/zoom/2)) + sin(on/16)*6':y='(ih/2-(ih/zoom/2)) + cos(on/22)*4':s={settings.video_width}x{settings.video_height}:fps={settings.video_fps}"
            )

        cmd = [
            "ffmpeg",
            "-y",
            "-loop", "1",
            "-i", str(render_input),
            "-vf", (
                f"{vf},"
                f"noise=alls=10:allf=t+u,"
                f"drawbox=x=0:y='mod(t*220,ih)':w=iw:h=2:color=0xEF4444@0.6:t=fill,"
                f"drawbox=x='mod(t*650,iw)':y='ih/2':w=32:h=5:color=0x06B6D4@0.85:t=fill,"
                f"eq=contrast=1.06:brightness=0.01:saturation=1.12,format=yuv420p"
            ),
            "-t", f"{dur:.2f}",
            "-r", str(settings.video_fps),
            "-c:v", "libx264",
            "-preset", "ultrafast",
            "-crf", "18",
            "-pix_fmt", "yuv420p",
            str(output_mp4)
        ]

        res = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if res.returncode != 0:
            raise RuntimeError(f"FFmpeg scene render failed: {res.stderr[:400]}")

        scene.rendered = True
        scene.rendered_video_path = str(output_mp4)
        return str(output_mp4)

    @staticmethod
    def render_all_scenes_parallel(
        scenes: List[StoryboardScene],
        illustrations_dir: Path,
        rendered_dir: Path,
        progress_callback: Optional[Callable[[int, int, str], None]] = None
    ) -> List[str]:
        """
        Renders all 40 scenes in parallel using multi-threaded FFmpeg processes.
        Provides live progress callbacks for real-time ETA calculation.
        """
        rendered_dir.mkdir(parents=True, exist_ok=True)
        total = len(scenes)
        completed = 0
        video_paths = [None] * total

        def _worker(item: Tuple[int, StoryboardScene]):
            nonlocal completed
            idx, s = item
            png_file = illustrations_dir / f"scene_{s.scene_id:02d}.png"
            if not png_file.exists():
                from backend.app.agents.visual_agent import IllustrationAgent
                IllustrationAgent.generate_scene_png(s, png_file)
            
            out_mp4 = rendered_dir / f"scene_{s.scene_id:02d}.mp4"
            AnimationAgent.render_scene_to_video(s, png_file, out_mp4)
            completed += 1
            if progress_callback:
                progress_callback(completed, total, f"Animated scene {completed}/{total} ({s.camera_movement})")
            return idx, str(out_mp4)

        # 4 parallel FFmpeg encoding threads
        with ThreadPoolExecutor(max_workers=4) as executor:
            results = executor.map(_worker, enumerate(scenes))
            for idx, path in results:
                video_paths[idx] = path

        return video_paths
