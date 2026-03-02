import { useState, useCallback } from "react";

const STORAGE_KEY = "rushour_balance";
const INITIAL_BALANCE = 1000;
const BANKRUPT_REFILL = 500;

function readBalance(): number {
  const stored = localStorage.getItem(STORAGE_KEY);
  return stored ? parseInt(stored, 10) : INITIAL_BALANCE;
}

export function useBalance() {
  const [balance, setBalance] = useState(readBalance);

  const updateBalance = useCallback((delta: number) => {
    setBalance((prev) => {
      const next = Math.max(0, prev + delta);
      localStorage.setItem(STORAGE_KEY, next.toString());
      return next;
    });
  }, []);

  const refillBalance = useCallback(() => {
    localStorage.setItem(STORAGE_KEY, BANKRUPT_REFILL.toString());
    setBalance(BANKRUPT_REFILL);
  }, []);

  return { balance, updateBalance, refillBalance };
}
