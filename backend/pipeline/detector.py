import numpy as np
import supervision as sv
from ultralytics import YOLO

CAR_CLASS_ID = 2  # COCO class ID for "car"


class CarDetectorTracker:
    def __init__(self, model_path: str = "yolov8n.pt", frame_rate: int = 30):
        self.model = YOLO(model_path)
        self.tracker = sv.ByteTrack(
            track_activation_threshold=0.25,
            lost_track_buffer=30,
            minimum_matching_threshold=0.8,
            frame_rate=frame_rate,
        )

    def detect_and_track(self, frame: np.ndarray) -> sv.Detections:
        """Run YOLO detection + ByteTrack on a single frame.

        Returns supervision Detections with tracker_id assigned.
        Only includes detections with class_id == CAR_CLASS_ID.
        """
        results = self.model(frame, verbose=False, device="cpu")[0]
        detections = sv.Detections.from_ultralytics(results)

        # Filter to cars only
        if len(detections) > 0 and detections.class_id is not None:
            car_mask = detections.class_id == CAR_CLASS_ID
            detections = detections[car_mask]

        # Apply ByteTrack tracking
        if len(detections) > 0:
            detections = self.tracker.update_with_detections(detections)

        return detections

    def reset(self):
        """Reset tracker state between clips."""
        self.tracker.reset()
