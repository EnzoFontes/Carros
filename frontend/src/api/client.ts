import axios from "axios";
import type { ClipData, GuessResponse, GameResult, GuessType } from "../types";

const api = axios.create({ baseURL: "/api" });

export async function fetchNextClip(): Promise<ClipData> {
  const { data } = await api.get<ClipData>("/clips/next");
  return data;
}

export async function submitGuess(
  clipId: number,
  guessType: GuessType,
  guessValue: string,
  betAmount: number
): Promise<GuessResponse> {
  const { data } = await api.post<GuessResponse>("/game/guess", {
    clip_id: clipId,
    guess_type: guessType,
    guess_value: guessValue,
    bet_amount: betAmount,
  });
  return data;
}

export async function fetchResult(gameId: string): Promise<GameResult> {
  const { data } = await api.get<GameResult>(`/game/result/${gameId}`);
  return data;
}
