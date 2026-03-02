import sqlite3
import json
from pathlib import Path
from app.config import DB_PATH

SCHEMA = """
CREATE TABLE IF NOT EXISTS clips (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    clip_name TEXT UNIQUE NOT NULL,
    raw_path TEXT NOT NULL,
    annotated_path TEXT NOT NULL,
    car_count INTEGER NOT NULL,
    frame_counts TEXT NOT NULL,
    zone_polygon TEXT NOT NULL,
    duration_seconds REAL NOT NULL,
    fps REAL NOT NULL,
    location_name TEXT DEFAULT 'Unknown Location',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS games (
    id TEXT PRIMARY KEY,
    clip_id INTEGER NOT NULL REFERENCES clips(id),
    guess_type TEXT NOT NULL,
    guess_value TEXT NOT NULL,
    bet_amount INTEGER NOT NULL,
    actual_count INTEGER NOT NULL,
    won BOOLEAN NOT NULL,
    payout INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""


def get_db() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db():
    conn = get_db()
    conn.executescript(SCHEMA)
    conn.close()


def save_clip(
    clip_name: str,
    raw_path: str,
    annotated_path: str,
    car_count: int,
    frame_counts: list[int],
    zone_polygon: list[list[int]],
    duration_seconds: float,
    fps: float,
    location_name: str = "Unknown Location",
):
    conn = get_db()
    conn.execute(
        """INSERT OR REPLACE INTO clips
           (clip_name, raw_path, annotated_path, car_count, frame_counts,
            zone_polygon, duration_seconds, fps, location_name)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            clip_name,
            str(raw_path),
            str(annotated_path),
            car_count,
            json.dumps(frame_counts),
            json.dumps(zone_polygon),
            duration_seconds,
            fps,
            location_name,
        ),
    )
    conn.commit()
    conn.close()


def get_random_clip() -> dict | None:
    conn = get_db()
    row = conn.execute("SELECT * FROM clips ORDER BY RANDOM() LIMIT 1").fetchone()
    conn.close()
    if row is None:
        return None
    return dict(row)


def get_clip_by_id(clip_id: int) -> dict | None:
    conn = get_db()
    row = conn.execute("SELECT * FROM clips WHERE id = ?", (clip_id,)).fetchone()
    conn.close()
    if row is None:
        return None
    return dict(row)


def save_game(game_id: str, clip_id: int, guess_type: str, guess_value: str,
              bet_amount: int, actual_count: int, won: bool, payout: int):
    conn = get_db()
    conn.execute(
        """INSERT INTO games (id, clip_id, guess_type, guess_value, bet_amount,
           actual_count, won, payout) VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (game_id, clip_id, guess_type, guess_value, bet_amount, actual_count, won, payout),
    )
    conn.commit()
    conn.close()


def get_game(game_id: str) -> dict | None:
    conn = get_db()
    row = conn.execute("SELECT * FROM games WHERE id = ?", (game_id,)).fetchone()
    conn.close()
    if row is None:
        return None
    return dict(row)
