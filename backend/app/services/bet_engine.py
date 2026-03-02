import random
from app.config import PAYOUTS
from app.models import BetOptions, UnderOverBet, RangeBet, ExactBet


def generate_bet_options(actual_count: int) -> BetOptions:
    """Generate dynamic bet brackets around the actual car count.

    Adds noise so the brackets don't trivially reveal the answer.
    """
    noise = random.randint(-2, 2)
    center = max(actual_count + noise, 3)

    range_width = max(2, actual_count // 4)
    range_low = max(0, center - range_width)
    range_high = center + range_width

    under_threshold = range_low
    over_threshold = range_high

    # Exact options: one near the low boundary, one near the high
    exact_low = max(0, range_low + random.randint(-1, 1))
    exact_high = max(exact_low + 1, range_high + random.randint(-1, 1))

    return BetOptions(
        under=UnderOverBet(
            label=f"Under {under_threshold}",
            threshold=under_threshold,
            payout=PAYOUTS["under"],
        ),
        range=RangeBet(
            label=f"{range_low}\u2013{range_high}",
            low=range_low,
            high=range_high,
            payout=PAYOUTS["range"],
        ),
        over=UnderOverBet(
            label=f"Over {over_threshold}",
            threshold=over_threshold,
            payout=PAYOUTS["over"],
        ),
        exact=[
            ExactBet(label=f"Exactly {exact_low}", value=exact_low, payout=PAYOUTS["exact"]),
            ExactBet(label=f"Exactly {exact_high}", value=exact_high, payout=PAYOUTS["exact"]),
        ],
    )


def evaluate_guess(
    guess_type: str,
    guess_value: str,
    actual_count: int,
    bet_options: BetOptions,
) -> bool:
    """Evaluate whether a guess is correct."""
    if guess_type == "under":
        return actual_count < bet_options.under.threshold
    elif guess_type == "over":
        return actual_count > bet_options.over.threshold
    elif guess_type == "range":
        return bet_options.range.low <= actual_count <= bet_options.range.high
    elif guess_type == "exact":
        return actual_count == int(guess_value)
    return False


def calculate_payout(guess_type: str, bet_amount: int) -> int:
    """Calculate payout for a winning bet."""
    multiplier = PAYOUTS.get(guess_type, 1.0)
    return int(bet_amount * multiplier)
