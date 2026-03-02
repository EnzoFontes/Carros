import json
from app.database import get_random_clip, get_clip_by_id
from app.services.bet_engine import generate_bet_options
from app.models import ClipResponse, BetOptions


def get_next_clip() -> ClipResponse | None:
    """Get a random clip with dynamically generated bet options."""
    clip = get_random_clip()
    if clip is None:
        return None

    bet_options = generate_bet_options(clip["car_count"])

    return ClipResponse(
        clip_id=clip["id"],
        clip_name=clip["clip_name"],
        location_name=clip["location_name"],
        duration_seconds=clip["duration_seconds"],
        preview_url=f"/thumbnails/{clip['clip_name']}.jpg",
        bet_options=bet_options,
    )


def get_clip_details(clip_id: int) -> dict | None:
    """Get full clip details including frame_counts and video path."""
    clip = get_clip_by_id(clip_id)
    if clip is None:
        return None
    clip["frame_counts"] = json.loads(clip["frame_counts"])
    return clip
