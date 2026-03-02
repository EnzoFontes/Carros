import { useState, useCallback } from "react";
import { fetchNextClip, submitGuess, fetchResult } from "../api/client";
import type {
  ClipData,
  GuessResponse,
  GameResult,
  GameState,
  GuessType,
} from "../types";

export function useGame() {
  const [state, setState] = useState<GameState>("idle");
  const [clip, setClip] = useState<ClipData | null>(null);
  const [guessData, setGuessData] = useState<GuessResponse | null>(null);
  const [result, setResult] = useState<GameResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const loadNextClip = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const nextClip = await fetchNextClip();
      setClip(nextClip);
      setGuessData(null);
      setResult(null);
      setState("betting");
    } catch (e: any) {
      setError(e.response?.data?.detail || "Failed to load clip");
    } finally {
      setLoading(false);
    }
  }, []);

  const placeBet = useCallback(
    async (guessType: GuessType, guessValue: string, betAmount: number) => {
      if (!clip) return;
      setLoading(true);
      setError(null);
      try {
        const response = await submitGuess(
          clip.clip_id,
          guessType,
          guessValue,
          betAmount
        );
        setGuessData(response);
        setState("playing");
      } catch (e: any) {
        setError(e.response?.data?.detail || "Failed to submit guess");
      } finally {
        setLoading(false);
      }
    },
    [clip]
  );

  const revealResult = useCallback(async () => {
    if (!guessData) return;
    setLoading(true);
    try {
      const gameResult = await fetchResult(guessData.game_id);
      setResult(gameResult);
      setState("result");
    } catch (e: any) {
      setError(e.response?.data?.detail || "Failed to get result");
    } finally {
      setLoading(false);
    }
  }, [guessData]);

  const playAgain = useCallback(() => {
    setState("idle");
    setClip(null);
    setGuessData(null);
    setResult(null);
  }, []);

  return {
    state,
    clip,
    guessData,
    result,
    error,
    loading,
    loadNextClip,
    placeBet,
    revealResult,
    playAgain,
  };
}
