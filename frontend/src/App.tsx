import { useEffect } from "react";
import { useGame } from "./hooks/useGame";
import { useBalance } from "./hooks/useBalance";
import { VideoPlayer } from "./components/VideoPlayer";
import { BettingPanel } from "./components/BettingPanel";
import { ResultModal } from "./components/ResultModal";
import { BalanceDisplay } from "./components/BalanceDisplay";
import type { GuessType } from "./types";
import "./styles/globals.css";

export default function App() {
  const game = useGame();
  const { balance, updateBalance, refillBalance } = useBalance();

  useEffect(() => {
    if (game.result) {
      if (game.result.won) {
        updateBalance(game.result.payout);
      } else {
        updateBalance(-game.result.bet_amount);
      }
    }
  }, [game.result]);

  const handlePlaceBet = (
    guessType: GuessType,
    guessValue: string,
    amount: number
  ) => {
    game.placeBet(guessType, guessValue, amount);
  };

  const handlePlayAgain = () => {
    game.playAgain();
  };

  return (
    <div className="app">
      <header className="header">
        <h1 className="header-title">RUSH<span>HOUR</span></h1>
        <BalanceDisplay balance={balance} onRefill={refillBalance} />
      </header>

      <div className="main-content">
        {/* Left: Video / Preview Area */}
        <div>
          {game.state === "idle" && !game.loading && (
            <div className="idle-screen">
              <button className="start-btn" onClick={game.loadNextClip}>
                START GAME
              </button>
            </div>
          )}

          {game.state === "idle" && game.loading && (
            <div className="idle-screen">
              <span className="loading-text">LOADING...</span>
            </div>
          )}

          {game.state === "betting" && game.clip && (
            <div className="preview-area">
              <img
                className="preview-image"
                src={game.clip.preview_url}
                alt={game.clip.location_name}
              />
              <div className="preview-overlay">
                <div className="preview-location">
                  {game.clip.location_name.toUpperCase()}
                </div>
                <span className="preview-badge">
                  {game.clip.duration_seconds.toFixed(0)}s clip
                </span>
              </div>
            </div>
          )}

          {game.state === "playing" && game.guessData && game.clip && (
            <VideoPlayer
              videoUrl={game.guessData.video_url}
              frameCounts={game.guessData.frame_counts}
              fps={game.guessData.fps}
              durationSeconds={game.guessData.duration_seconds}
              locationName={game.clip.location_name}
              onEnded={game.revealResult}
            />
          )}

          {game.state === "result" && game.guessData && game.clip && (
            <VideoPlayer
              videoUrl={game.guessData.video_url}
              frameCounts={game.guessData.frame_counts}
              fps={game.guessData.fps}
              durationSeconds={game.guessData.duration_seconds}
              locationName={game.clip.location_name}
              onEnded={() => {}}
            />
          )}
        </div>

        {/* Right: Betting Panel / Status */}
        <div>
          {game.state === "betting" && game.clip && (
            <BettingPanel
              betOptions={game.clip.bet_options}
              balance={balance}
              onPlaceBet={handlePlaceBet}
              loading={game.loading}
            />
          )}

          {(game.state === "idle" || game.state === "playing") && (
            <div className="waiting-panel">
              {game.state === "idle" && "PRESS START"}
              {game.state === "playing" && "WATCHING..."}
            </div>
          )}

          {game.state === "result" && (
            <div className="waiting-panel">ROUND COMPLETE</div>
          )}
        </div>
      </div>

      {game.error && <div className="error-msg">{game.error}</div>}

      {game.state === "result" && game.result && (
        <ResultModal result={game.result} onPlayAgain={handlePlayAgain} />
      )}
    </div>
  );
}
