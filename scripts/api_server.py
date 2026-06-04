from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os
import asyncio
import subprocess
import sys

app = FastAPI(title="RotarySlider Feature Studio API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class IntentPayload(BaseModel):
    target: str
    name: str
    metric: str

@app.get("/status")
def get_status(target: str):
    map_path = os.path.join(target, 'feature_map.json')
    if os.path.exists(map_path):
        with open(map_path, 'r') as f:
            return json.load(f)
    return {"features": []}

@app.post("/intent")
def inject_intent(payload: IntentPayload):
    cli_path = os.path.join(os.path.dirname(__file__), 'cli.py')
    subprocess.run([sys.executable, cli_path, 'intent', payload.target, '--name', payload.name, '--metric', payload.metric])
    return {"status": "success", "message": "Intent injected."}

@app.get("/gallery")
def get_gallery():
    return {
        "items": [
            {"id": 1, "component": "Hero Navigation", "grade": "PASS", "heuristics": "Contrast 4.5:1", "timestamp": "2026-06-04T12:00:00Z"},
            {"id": 2, "component": "Auth Modal", "grade": "FAIL", "heuristics": "Padding inconsistent", "timestamp": "2026-06-04T12:05:00Z"}
        ]
    }

@app.websocket("/telemetry")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        epoch = 1
        while True:
            await websocket.send_json({
                "epoch": epoch,
                "cpu_allocated": 2,
                "vram_status": "Time-Slicing Active",
                "message": f"Matrix executing epoch {epoch}..."
            })
            epoch += 1
            await asyncio.sleep(2)
    except Exception:
        pass
