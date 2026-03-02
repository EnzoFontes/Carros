from fastapi import APIRouter, HTTPException
from app.services.clip_service import get_next_clip
from app.models import ClipResponse

router = APIRouter()


@router.get("/next", response_model=ClipResponse)
def next_clip():
    """Get the next clip to play with bet options."""
    clip = get_next_clip()
    if clip is None:
        raise HTTPException(status_code=404, detail="No clips available. Run the pipeline first.")
    return clip
