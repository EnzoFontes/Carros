import json
import subprocess
import sys
from pathlib import Path

import numpy as np

# Add backend to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pipeline.video_io import get_video_info, iter_frames, VideoWriter
from pipeline.zone import auto_detect_zone, full_frame_zone, load_zone_from_json
from pipeline.detector import CarDetectorTracker
from pipeline.counter import ZoneEntryCounter
from pipeline.annotator import ClipAnnotator
from app.database import init_db, save_clip


def process_single_clip(
    raw_path: Path,
    output_dir: Path,
    model_path: str = "yolov8n.pt",
    location_name: str = "Unknown Location",
) -> dict:
    """Process a single video clip: detect cars, count entries, render annotated video."""
    print(f"\n{'='*60}")
    print(f"Processing: {raw_path.name}")
    print(f"{'='*60}")

    # Get video info
    info = get_video_info(raw_path)
    print(f"  Resolution: {info['width']}x{info['height']}")
    print(f"  FPS: {info['fps']:.1f}, Duration: {info['duration_seconds']:.1f}s")
    print(f"  Total frames: {info['frame_count']}")

    fps = info["fps"]
    w, h = info["width"], info["height"]
    total_frames = info["frame_count"]

    # Check for manual zone file first, then auto-detect
    manual_zone_path = raw_path.with_suffix(".zone.json")
    if manual_zone_path.exists():
        print(f"  Loading manual zone from {manual_zone_path.name}...")
        zone_polygon = load_zone_from_json(manual_zone_path)
        print(f"  Manual zone loaded: {len(zone_polygon)} vertices")
    else:
        print("  Detecting road zone...")
        try:
            zone_polygon = auto_detect_zone(raw_path)
            print(f"  Zone detected: {len(zone_polygon)} vertices")
        except Exception as e:
            print(f"  Zone detection failed ({e}), using full frame")
            zone_polygon = full_frame_zone(w, h)

    # Initialize detector, counter, annotator
    detector = CarDetectorTracker(model_path=model_path, frame_rate=int(fps))
    counter = ZoneEntryCounter(zone_polygon)
    annotator = ClipAnnotator(zone_polygon)

    # Output paths
    clip_name = raw_path.stem
    temp_path = output_dir / f"{clip_name}_temp.mp4"
    final_path = output_dir / f"{clip_name}_annotated.mp4"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Process frames
    print("  Processing frames...")
    with VideoWriter(temp_path, fps, w, h) as writer:
        for frame_idx, frame in enumerate(iter_frames(raw_path)):
            # Detect and track
            detections = detector.detect_and_track(frame)

            # Count zone entries
            count = counter.update(detections)

            # Calculate time remaining
            time_remaining = max(0, (total_frames - frame_idx) / fps)

            # Annotate frame
            annotated = annotator.annotate_frame(
                frame, detections, count, time_remaining, location_name
            )
            writer.write(annotated)

            # Progress
            if frame_idx % 30 == 0:
                pct = (frame_idx / total_frames) * 100
                print(f"    Frame {frame_idx}/{total_frames} ({pct:.0f}%) - Cars: {count}")

    print(f"  Final car count: {counter.current_count}")

    # Re-encode with ffmpeg for browser compatibility
    _reencode_video(temp_path, final_path)

    # Save to database
    save_clip(
        clip_name=clip_name,
        raw_path=str(raw_path),
        annotated_path=str(final_path),
        car_count=counter.current_count,
        frame_counts=counter.frame_counts,
        zone_polygon=zone_polygon.tolist(),
        duration_seconds=info["duration_seconds"],
        fps=fps,
        location_name=location_name,
    )

    print(f"  Saved: {final_path}")
    return {
        "clip_name": clip_name,
        "car_count": counter.current_count,
        "annotated_path": str(final_path),
    }


def _get_ffmpeg_path() -> str:
    """Find ffmpeg binary — system PATH or imageio_ffmpeg fallback."""
    import shutil
    path = shutil.which("ffmpeg")
    if path:
        return path
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        return ""


def _reencode_video(input_path: Path, output_path: Path):
    """Re-encode video with ffmpeg for browser playback compatibility."""
    ffmpeg = _get_ffmpeg_path()
    if not ffmpeg:
        print("  Warning: ffmpeg not found, using raw OpenCV output (may not play in all browsers)")
        input_path.rename(output_path)
        return
    try:
        subprocess.run(
            [
                ffmpeg, "-y", "-i", str(input_path),
                "-c:v", "libx264", "-crf", "23", "-preset", "medium",
                "-movflags", "+faststart",
                "-an",  # no audio
                str(output_path),
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        input_path.unlink()  # remove temp file
        print(f"  Re-encoded with ffmpeg: {output_path.name}")
    except subprocess.CalledProcessError as e:
        print(f"  Warning: ffmpeg failed ({e}), using raw OpenCV output")
        input_path.rename(output_path)


def process_all_clips(
    input_dir: Path,
    output_dir: Path,
    model_path: str = "yolov8n.pt",
):
    """Batch process all video clips in a directory."""
    init_db()

    video_extensions = {".mp4", ".avi", ".mov", ".mkv", ".webm"}
    clips = sorted(
        f for f in input_dir.iterdir()
        if f.suffix.lower() in video_extensions
    )

    if not clips:
        print(f"No video files found in {input_dir}")
        return

    print(f"Found {len(clips)} video(s) to process")
    results = []

    for clip_path in clips:
        result = process_single_clip(
            raw_path=clip_path,
            output_dir=output_dir,
            model_path=model_path,
            location_name=clip_path.stem.replace("_", " ").title(),
        )
        results.append(result)

    print(f"\n{'='*60}")
    print(f"DONE - Processed {len(results)} clips")
    for r in results:
        print(f"  {r['clip_name']}: {r['car_count']} cars -> {r['annotated_path']}")
