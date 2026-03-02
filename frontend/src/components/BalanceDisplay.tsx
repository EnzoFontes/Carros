interface BalanceDisplayProps {
  balance: number;
  onRefill: () => void;
}

export function BalanceDisplay({ balance, onRefill }: BalanceDisplayProps) {
  return (
    <div className="balance-display">
      <span className="coin-icon gold">&#9679;</span>
      <span className="balance-amount">{balance.toLocaleString()}</span>
      {balance === 0 && (
        <button className="refill-btn" onClick={onRefill}>
          GET 500 FREE
        </button>
      )}
    </div>
  );
}
