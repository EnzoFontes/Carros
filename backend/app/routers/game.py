import uuid
from pathlib import Path
from fastapi import APIRouter, HTTPException
from app.models import GuessRequest, GuessResponse, ResultResponse
from app.services.clip_service import get_clip_details
from app.services.bet_engine import generate_bet_options, evaluate_guess, calculate_payout
from app.database import save_game, get_game

router = APIRouter()

# In-memory cache for active game bet_options (so evaluation uses same brackets)
_active_games: dict[str, dict] = {}


@router.post("/guess", response_model=GuessResponse)
def submit_guess(req: GuessRequest):
    """Submit a guess for a clip. Returns the annotated video URL."""
    clip = get_clip_details(req.clip_id)
    if clip is None:
        raise HTTPException(status_code=404, detail="Clip not found")

    game_id = str(uuid.uuid4())

    # Regenerate bet options for evaluation (same logic, seeded per game)
    bet_options = generate_bet_options(clip["car_count"])

    # Evaluate the guess
    won = evaluate_guess(req.guess_type, req.guess_value, clip["car_count"], bet_options)
    payout = calculate_payout(req.guess_type, req.bet_amount) if won else 0

    # Save game
    save_game(
        game_id=game_id,
        clip_id=req.clip_id,
        guess_type=req.guess_type,
        guess_value=req.guess_value,
        bet_amount=req.bet_amount,
        actual_count=clip["car_count"],
        won=won,
        payout=payout,
    )

    # Build video URL from annotated path
    annotated_name = Path(clip["annotated_path"]).name
    video_url = f"/videos/{annotated_name}"

    return GuessResponse(
        game_id=game_id,
        video_url=video_url,
        frame_counts=clip["frame_counts"],
        fps=clip["fps"],
        duration_seconds=clip["duration_seconds"],
    )


@router.get("/result/{game_id}", response_model=ResultResponse)
def get_result(game_id: str):
    """Get the result of a game after watching the clip."""
    game = get_game(game_id)
    if game is None:
        raise HTTPException(status_code=404, detail="Game not found")

    return ResultResponse(
        won=bool(game["won"]),
        actual_count=game["actual_count"],
        guess_type=game["guess_type"],
        payout=game["payout"],
        bet_amount=game["bet_amount"],
    )
