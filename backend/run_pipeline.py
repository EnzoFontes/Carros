#!/usr/bin/env python3
"""Batch process raw traffic video clips for Rush Hour game.

Usage:
    python run_pipeline.py
    python run_pipeline.py --input data/raw --output data/processed --model yolov8n.pt
"""
import argparse
import sys
from pathlib import Path

# Ensure backend is on the path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from pipeline.process_clips import process_all_clips
from app.config import RAW_DIR, PROCESSED_DIR, YOLO_MODEL


def main():
    parser = argparse.ArgumentParser(description="Process traffic clips for Rush Hour")
    parser.add_argument("--input", type=Path, default=RAW_DIR, help="Input directory with raw videos")
    parser.add_argument("--output", type=Path, default=PROCESSED_DIR, help="Output directory for annotated videos")
    parser.add_argument("--model", type=str, default=YOLO_MODEL, help="YOLO model path (default: yolov8n.pt)")
    args = parser.parse_args()

    if not args.input.exists():
        print(f"Error: Input directory does not exist: {args.input}")
        sys.exit(1)

    process_all_clips(args.input, args.output, args.model)


if __name__ == "__main__":
    main()
