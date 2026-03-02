from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import numpy as np
import io
import os
import cv2
from ultralytics import YOLO

app = FastAPI(title="Wheel Try-On API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL_PATH = "models/wheel.pt"
_model = None

def get_model():
    """Load YOLO model if present. If weights are missing, return None so the API can still run."""
    global _model
    if _model is None:
        if not os.path.exists(MODEL_PATH):
            return None
        _model = YOLO(MODEL_PATH)
    return _model

def pil_to_bgr(pil_img: Image.Image) -> np.ndarray:
    rgb = np.array(pil_img.convert("RGB"))
    return cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/detect-wheels")
async def detect_wheels(car: UploadFile = File(...)):
    content = await car.read()
    img = Image.open(io.BytesIO(content)).convert("RGB")
    bgr = pil_to_bgr(img)
    h, w = bgr.shape[:2]

    model = get_model()
    if model is None:
        # No weights yet — return empty detections so you can test the website end-to-end.
        return {"image": {"w": w, "h": h}, "wheels": []}
    results = model.predict(bgr, conf=0.25, verbose=False)

    dets = []
    for r in results:
        if r.boxes is None:
            continue
        for b in r.boxes:
            xyxy = b.xyxy[0].cpu().numpy().tolist()
            conf = float(b.conf[0].cpu().numpy().item())
            x1, y1, x2, y2 = xyxy
            cx = (x1 + x2) / 2.0
            cy = (y1 + y2) / 2.0
            rad = min((x2 - x1), (y2 - y1)) / 2.0
            dets.append({"cx": cx, "cy": cy, "r": rad, "conf": conf})

    if not dets:
        return {"image": {"w": w, "h": h}, "wheels": []}

    dets.sort(key=lambda d: d["conf"], reverse=True)
    top = dets[:2]
    top.sort(key=lambda d: d["cx"])

    return {"image": {"w": w, "h": h}, "wheels": top}
