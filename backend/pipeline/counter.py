import numpy as np
import supervision as sv
from typing import Set


class ZoneEntryCounter:
    """Counts unique cars entering a polygon zone.

    Each car (tracked by ByteTrack ID) is counted exactly once
    when its bottom-center point enters the zone.
    """

    def __init__(self, zone_polygon: np.ndarray):
        self.zone = sv.PolygonZone(
            polygon=zone_polygon,
            triggering_anchors=[sv.Position.BOTTOM_CENTER],
        )
        self.counted_ids: Set[int] = set()
        self.current_count: int = 0
        self.frame_counts: list[int] = []

    def update(self, detections: sv.Detections) -> int:
        """Process one frame of detections. Returns running total of unique cars."""
        # Check which detections are inside the zone
        in_zone_mask = self.zone.trigger(detections=detections)
        in_zone = detections[in_zone_mask]

        # Count new tracker IDs
        if in_zone.tracker_id is not None:
            for tid in in_zone.tracker_id:
                if tid not in self.counted_ids:
                    self.counted_ids.add(tid)
                    self.current_count += 1

        self.frame_counts.append(self.current_count)
        return self.current_count

    def reset(self):
        self.counted_ids.clear()
        self.current_count = 0
        self.frame_counts.clear()
