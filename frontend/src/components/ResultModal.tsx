import type { GameResult } from "../types";

interface ResultModalProps {
  result: GameResult;
  onPlayAgain: () => void;
}

export function ResultModal({ result, onPlayAgain }: ResultModalProps) {
  const won = result.won;

  return (
    <div className={`result-overlay ${won ? "result-win" : "result-lose"}`}>
      <div className="result-card">
        <div className="result-icon">{won ? "\u{1F3C6}" : "\u274C"}</div>
        <h2 className="result-title">
          {won ? "YOU WIN!" : "BETTER LUCK NEXT TIME"}
        </h2>

        <div className="result-details">
          <div className="result-row">
            <span>Actual count</span>
            <span className="result-value">{result.actual_count}</span>
          </div>
          <div className="result-row">
            <span>Your bet</span>
            <span className="result-value">{result.guess_type.toUpperCase()}</span>
          </div>
          <div className="result-row">
            <span>Wagered</span>
            <span className="result-value">{result.bet_amount}</span>
          </div>
          {won && (
            <div className="result-row">
              <span>Payout</span>
              <span className="result-value payout-value">+{result.payout}</span>
            </div>
          )}
          {!won && (
            <div className="result-row">
              <span>Lost</span>
              <span className="result-value loss-value">-{result.bet_amount}</span>
            </div>
          )}
        </div>

        <button className="play-again-btn" onClick={onPlayAgain}>
          Play Again
        </button>
      </div>
    </div>
  );
}
