from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
THUMBNAILS_DIR = DATA_DIR / "thumbnails"
DB_PATH = DATA_DIR / "rushour.db"

YOLO_MODEL = "yolov8n.pt"
CAR_CLASS_ID = 2  # COCO "car"

PAYOUTS = {
    "under": 2.0,
    "over": 2.0,
    "range": 3.0,
    "exact": 5.0,
}

INITIAL_BALANCE = 1000
MIN_BET = 10
