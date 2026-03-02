import { useState } from "react";
import type { BetOptions, GuessType } from "../types";

interface BettingPanelProps {
  betOptions: BetOptions;
  balance: number;
  onPlaceBet: (guessType: GuessType, guessValue: string, amount: number) => void;
  loading: boolean;
}

export function BettingPanel({
  betOptions,
  balance,
  onPlaceBet,
  loading,
}: BettingPanelProps) {
  const [selectedType, setSelectedType] = useState<GuessType | null>(null);
  const [selectedExactValue, setSelectedExactValue] = useState<string>("");
  const [betAmount, setBetAmount] = useState(Math.min(100, balance));

  const handleSubmit = () => {
    if (!selectedType) return;
    let guessValue = "";
    if (selectedType === "exact") {
      guessValue = selectedExactValue;
    }
    onPlaceBet(selectedType, guessValue, betAmount);
  };

  const maxBet = balance;
  const canBet = selectedType !== null && betAmount > 0 && betAmount <= balance;

  const quickAmounts = [25, 50, 100, 250].filter((a) => a <= balance);

  return (
    <div className="betting-panel">
      <h2 className="betting-title">Place your bet</h2>

      <div className="bet-options">
        {/* Under */}
        <button
          className={`bet-card bet-under ${selectedType === "under" ? "selected" : ""}`}
          onClick={() => { setSelectedType("under"); setSelectedExactValue(""); }}
        >
          <span className="bet-icon">&#9660;</span>
          <div className="bet-info">
            <div className="bet-label">{betOptions.under.label}</div>
            <div className="bet-sublabel">Under threshold</div>
          </div>
          <span className="bet-payout">{betOptions.under.payout}x</span>
        </button>

        {/* Range */}
        <button
          className={`bet-card bet-range ${selectedType === "range" ? "selected" : ""}`}
          onClick={() => { setSelectedType("range"); setSelectedExactValue(""); }}
        >
          <span className="bet-icon">&#8596;</span>
          <div className="bet-info">
            <div className="bet-label">{betOptions.range.label}</div>
            <div className="bet-sublabel">Within range</div>
          </div>
          <span className="bet-payout">{betOptions.range.payout}x</span>
        </button>

        {/* Over */}
        <button
          className={`bet-card bet-over ${selectedType === "over" ? "selected" : ""}`}
          onClick={() => { setSelectedType("over"); setSelectedExactValue(""); }}
        >
          <span className="bet-icon">&#9650;</span>
          <div className="bet-info">
            <div className="bet-label">{betOptions.over.label}</div>
            <div className="bet-sublabel">Over threshold</div>
          </div>
          <span className="bet-payout">{betOptions.over.payout}x</span>
        </button>

        {/* Exact options */}
        {betOptions.exact.map((ex) => (
          <button
            key={ex.value}
            className={`bet-card bet-exact ${selectedType === "exact" && selectedExactValue === String(ex.value) ? "selected" : ""}`}
            onClick={() => { setSelectedType("exact"); setSelectedExactValue(String(ex.value)); }}
          >
            <span className="bet-icon">&#9733;</span>
            <div className="bet-info">
              <div className="bet-label">{ex.label}</div>
              <div className="bet-sublabel">Exact count</div>
            </div>
            <span className="bet-payout">{ex.payout}x</span>
          </button>
        ))}
      </div>

      <div className="bet-amount-section">
        <div className="bet-amount-label">
          <span>Wager</span>
          <span className="bet-amount-value-inline">{betAmount}</span>
        </div>
        <input
          type="range"
          min={10}
          max={maxBet}
          step={10}
          value={betAmount}
          onChange={(e) => setBetAmount(Number(e.target.value))}
          className="bet-slider"
        />
        {quickAmounts.length > 0 && (
          <div className="bet-quick-amounts">
            {quickAmounts.map((amt) => (
              <button
                key={amt}
                className={`bet-quick-btn ${betAmount === amt ? "active" : ""}`}
                onClick={() => setBetAmount(amt)}
              >
                {amt}
              </button>
            ))}
          </div>
        )}
      </div>

      <button
        className="place-bet-btn"
        onClick={handleSubmit}
        disabled={!canBet || loading}
      >
        {loading ? "Placing..." : "Place Bet"}
      </button>
    </div>
  );
}
