from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import os

from app.config import PROCESSED_DIR, THUMBNAILS_DIR
from app.database import init_db
from app.routers import clips, game

app = FastAPI(title="Rush Hour API", version="1.0.0")

# Configure CORS based on environment
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
if ENVIRONMENT == "production":
    # Allow requests from Render deployment domain
    allow_origins = ["*"]  # Adjust this to specific domain when deployed
else:
    allow_origins = ["http://localhost:3000", "http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    init_db()


@app.get("/api/health")
def health():
    return {"status": "ok"}


# API routers (registered BEFORE static mount to avoid route conflicts)
app.include_router(clips.router, prefix="/api/clips", tags=["clips"])
app.include_router(game.router, prefix="/api/game", tags=["game"])

# Serve static files (mount LAST — they're catch-alls)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
THUMBNAILS_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/thumbnails", StaticFiles(directory=str(THUMBNAILS_DIR)), name="thumbnails")
app.mount("/videos", StaticFiles(directory=str(PROCESSED_DIR)), name="videos")

# Serve frontend build files
frontend_build_path = Path(__file__).resolve().parent.parent.parent / "frontend" / "dist"
if frontend_build_path.exists():
    app.mount("/", StaticFiles(directory=str(frontend_build_path), html=True), name="frontend")
