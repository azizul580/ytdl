from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import json

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "YouTube Downloader API is running."}

@app.get("/info")
def get_video_info(url: str):
    try:
        result = subprocess.run(
            ["yt-dlp", "-j", url],
            capture_output=True,
            text=True,
            check=True
        )
        video_info = json.loads(result.stdout)
        return {
            "title": video_info.get("title"),
            "formats": [
                {
                    "format_id": f.get("format_id"),
                    "ext": f.get("ext"),
                    "resolution": f.get("format_note"),
                    "filesize_mb": round(f.get("filesize", 0) / 1048576, 2) if f.get("filesize") else None,
                    "url": f.get("url")
                }
                for f in video_info.get("formats", [])
                if f.get("filesize")
            ]
        }
    except subprocess.CalledProcessError as e:
        return {"error": "Failed to fetch video info."}
