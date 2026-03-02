import cv2
import numpy as np
from pathlib import Path
from .video_io import iter_frames


def sample_frames_evenly(path: str | Path, count: int = 30) -> list[np.ndarray]:
    cap = cv2.VideoCapture(str(path))
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    indices = np.linspace(0, total - 1, count, dtype=int)
    frames = []
    for idx in indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ret, frame = cap.read()
        if ret:
            frames.append(frame)
    cap.release()
    return frames


def auto_detect_zone(video_path: str | Path, sample_count: int = 30) -> np.ndarray:
    """Detect the road/traffic area by analyzing motion across sampled frames.

    Returns a polygon as np.ndarray of shape (N, 2) with integer coordinates.
    """
    frames = sample_frames_evenly(video_path, sample_count)
    if len(frames) < 3:
        raise ValueError("Not enough frames to detect zone")

    # Compute median background
    stack = np.stack(frames, axis=0)
    median_bg = np.median(stack, axis=0).astype(np.uint8)

    # Build motion mask from frame differences
    h, w = median_bg.shape[:2]
    motion_mask = np.zeros((h, w), dtype=np.uint8)
    for frame in frames:
        diff = cv2.absdiff(frame, median_bg)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 25, 255, cv2.THRESH_BINARY)
        motion_mask = cv2.bitwise_or(motion_mask, thresh)

    # Morphological cleanup
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 30))
    motion_mask = cv2.morphologyEx(motion_mask, cv2.MORPH_CLOSE, kernel)
    motion_mask = cv2.morphologyEx(motion_mask, cv2.MORPH_OPEN, kernel)

    # Find largest contour -> approximate polygon
    contours, _ = cv2.findContours(motion_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return full_frame_zone(w, h)

    largest = max(contours, key=cv2.contourArea)
    min_area = h * w * 0.05  # zone must be at least 5% of frame
    if cv2.contourArea(largest) < min_area:
        return full_frame_zone(w, h)

    epsilon = 0.02 * cv2.arcLength(largest, True)
    polygon = cv2.approxPolyDP(largest, epsilon, True)
    return polygon.reshape(-1, 2)


def full_frame_zone(width: int, height: int, margin: int = 10) -> np.ndarray:
    """Fallback: use entire frame as detection zone with a small margin."""
    return np.array([
        [margin, margin],
        [width - margin, margin],
        [width - margin, height - margin],
        [margin, height - margin],
    ])


def load_zone_from_json(path: str | Path) -> np.ndarray:
    """Load a manually defined zone polygon from a JSON file."""
    import json
    with open(path) as f:
        points = json.load(f)
    return np.array(points, dtype=np.int32)
