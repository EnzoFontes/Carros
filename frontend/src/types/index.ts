export interface UnderOverBet {
  label: string;
  threshold: number;
  payout: number;
}

export interface RangeBet {
  label: string;
  low: number;
  high: number;
  payout: number;
}

export interface ExactBet {
  label: string;
  value: number;
  payout: number;
}

export interface BetOptions {
  under: UnderOverBet;
  range: RangeBet;
  over: UnderOverBet;
  exact: ExactBet[];
}

export interface ClipData {
  clip_id: number;
  clip_name: string;
  location_name: string;
  duration_seconds: number;
  preview_url: string;
  bet_options: BetOptions;
}

export interface GuessResponse {
  game_id: string;
  video_url: string;
  frame_counts: number[];
  fps: number;
  duration_seconds: number;
}

export interface GameResult {
  won: boolean;
  actual_count: number;
  guess_type: string;
  payout: number;
  bet_amount: number;
}

export type GuessType = "under" | "range" | "over" | "exact";

export type GameState = "idle" | "betting" | "playing" | "result";
