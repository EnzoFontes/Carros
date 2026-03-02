import cv2
import numpy as np
from pathlib import Path
from typing import Generator


def get_video_info(path: str | Path) -> dict:
    cap = cv2.VideoCapture(str(path))
    if not cap.isOpened():
        raise ValueError(f"Cannot open video: {path}")
    info = {
        "fps": cap.get(cv2.CAP_PROP_FPS),
        "width": int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        "height": int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        "frame_count": int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
    }
    info["duration_seconds"] = info["frame_count"] / info["fps"] if info["fps"] > 0 else 0
    cap.release()
    return info


def iter_frames(path: str | Path) -> Generator[np.ndarray, None, None]:
    cap = cv2.VideoCapture(str(path))
    if not cap.isOpened():
        raise ValueError(f"Cannot open video: {path}")
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            yield frame
    finally:
        cap.release()


class VideoWriter:
    def __init__(self, path: str | Path, fps: float, width: int, height: int):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        self.writer = cv2.VideoWriter(str(self.path), fourcc, fps, (width, height))
        if not self.writer.isOpened():
            raise ValueError(f"Cannot create video writer: {path}")

    def write(self, frame: np.ndarray):
        self.writer.write(frame)

    def close(self):
        self.writer.release()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
