from pydantic import BaseModel


class BetOption(BaseModel):
    label: str
    payout: float


class UnderOverBet(BetOption):
    threshold: int


class RangeBet(BetOption):
    low: int
    high: int


class ExactBet(BetOption):
    value: int


class BetOptions(BaseModel):
    under: UnderOverBet
    range: RangeBet
    over: UnderOverBet
    exact: list[ExactBet]


class ClipResponse(BaseModel):
    clip_id: int
    clip_name: str
    location_name: str
    duration_seconds: float
    preview_url: str
    bet_options: BetOptions


class GuessRequest(BaseModel):
    clip_id: int
    guess_type: str  # "under", "range", "over", "exact"
    guess_value: str  # e.g. "10" for exact, or ignored for under/over/range
    bet_amount: int


class GuessResponse(BaseModel):
    game_id: str
    video_url: str
    frame_counts: list[int]
    fps: float
    duration_seconds: float


class ResultResponse(BaseModel):
    won: bool
    actual_count: int
    guess_type: str
    payout: int
    bet_amount: int
