import cv2
import numpy as np
import supervision as sv


class ClipAnnotator:
    """Renders bounding boxes, zone overlay, and car count HUD on video frames."""

    def __init__(self, zone_polygon: np.ndarray):
        self.zone_polygon = zone_polygon
        self.box_annotator = sv.BoxAnnotator(thickness=2)
        self.label_annotator = sv.LabelAnnotator(
            text_position=sv.Position.TOP_LEFT,
            text_scale=0.5,
            text_thickness=1,
        )

    def annotate_frame(
        self,
        frame: np.ndarray,
        detections: sv.Detections,
        count: int,
        time_remaining: float,
        location_name: str = "",
    ) -> np.ndarray:
        annotated = frame.copy()

        # Draw zone polygon (yellow semi-transparent fill)
        overlay = annotated.copy()
        cv2.fillPoly(overlay, [self.zone_polygon], color=(0, 255, 255))
        cv2.addWeighted(overlay, 0.12, annotated, 0.88, 0, annotated)
        cv2.polylines(annotated, [self.zone_polygon], True, (0, 255, 255), 2)

        # Draw bounding boxes
        if len(detections) > 0:
            annotated = self.box_annotator.annotate(scene=annotated, detections=detections)
            if detections.tracker_id is not None:
                labels = [f"#{tid}" for tid in detections.tracker_id]
                annotated = self.label_annotator.annotate(
                    scene=annotated, detections=detections, labels=labels
                )

        # HUD overlay
        h, w = annotated.shape[:2]
        self._draw_hud(annotated, count, time_remaining, location_name, w, h)

        return annotated

    def _draw_hud(
        self, frame: np.ndarray, count: int, time_remaining: float,
        location_name: str, w: int, h: int
    ):
        # Dark semi-transparent bar at top
        bar_h = 60
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (w, bar_h), (10, 14, 23), -1)
        cv2.addWeighted(overlay, 0.75, frame, 0.25, 0, frame)

        # Location name (top-left)
        if location_name:
            cv2.putText(
                frame, location_name.upper(),
                (15, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (200, 200, 200), 1,
            )

        # Vehicle count (top-right, large)
        count_text = str(count)
        (tw, th), _ = cv2.getTextSize(count_text, cv2.FONT_HERSHEY_SIMPLEX, 1.5, 3)
        cv2.putText(
            frame, count_text,
            (w - tw - 20, 45), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 136), 3,
        )
        cv2.putText(
            frame, "VEHICLES",
            (w - tw - 20, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (136, 146, 164), 1,
        )

        # Timer (below count)
        timer_text = f"{time_remaining:.0f}s"
        cv2.putText(
            frame, timer_text,
            (w - 55, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (136, 146, 164), 1,
        )

        # Progress bar at bottom of HUD bar
        progress_w = w - 30
        cv2.rectangle(frame, (15, bar_h - 5), (15 + progress_w, bar_h - 2), (40, 50, 70), -1)
