from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import json
import os
import asyncio

app = FastAPI(title="RotarySlider Feature Studio API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/status")
def get_status(target: str):
    """Returns the current tally state."""
    map_path = os.path.join(target, 'feature_map.json')
    if os.path.exists(map_path):
        with open(map_path, 'r') as f:
            return json.load(f)
    return {"features": []}

@app.websocket("/telemetry")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    # Mocking high-frequency telemetry stream for the Svelte dashboard
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
