import { useRef, useState, useEffect } from "react";

interface VideoPlayerProps {
  videoUrl: string;
  frameCounts: number[];
  fps: number;
  durationSeconds: number;
  locationName: string;
  onEnded: () => void;
}

export function VideoPlayer({
  videoUrl,
  frameCounts,
  fps,
  durationSeconds,
  locationName,
  onEnded,
}: VideoPlayerProps) {
  const videoRef = useRef<HTMLVideoElement>(null);
  const [currentCount, setCurrentCount] = useState(0);
  const [timeRemaining, setTimeRemaining] = useState(durationSeconds);
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    const video = videoRef.current;
    if (!video) return;

    const handleTimeUpdate = () => {
      const currentTime = video.currentTime;
      const frameIndex = Math.min(
        Math.floor(currentTime * fps),
        frameCounts.length - 1
      );
      if (frameIndex >= 0 && frameIndex < frameCounts.length) {
        setCurrentCount(frameCounts[frameIndex]);
      }
      setTimeRemaining(Math.max(0, durationSeconds - currentTime));
      setProgress((currentTime / durationSeconds) * 100);
    };

    video.addEventListener("timeupdate", handleTimeUpdate);
    video.play().catch(() => {});

    return () => video.removeEventListener("timeupdate", handleTimeUpdate);
  }, [fps, frameCounts, durationSeconds]);

  return (
    <div className="video-container">
      <video
        ref={videoRef}
        src={videoUrl}
        onEnded={onEnded}
        muted
        playsInline
        className="video-player"
      />
      <div className="video-hud">
        <div className="hud-top">
          <span className="hud-location">{locationName.toUpperCase()}</span>
          <div className="hud-count-area">
            <span className="hud-count">{currentCount}</span>
            <span className="hud-label">VEHICLES</span>
            <span className="hud-timer">{timeRemaining.toFixed(0)}s</span>
          </div>
        </div>
        <div className="hud-progress-bar">
          <div
            className="hud-progress-fill"
            style={{ width: `${progress}%` }}
          />
        </div>
      </div>
    </div>
  );
}
