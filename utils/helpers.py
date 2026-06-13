import pandas as pd
import streamlit as st
from datetime import datetime
import os
import numpy as np

DETECTIONS_CSV = "data/detections.csv"

def init_detections_db():
    """Create CSV file if not exists."""
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(DETECTIONS_CSV):
        df = pd.DataFrame(columns=[
            "timestamp", "video_name", "prediction", "confidence",
            "risk_level", "processing_time_sec", "avg_probability"
        ])
        df.to_csv(DETECTIONS_CSV, index=False)

def save_detection(video_name: str, prediction: str, confidence: float,
                   risk_level: str, processing_time: float, avg_prob: float):
    """Save detection result to CSV."""
    init_detections_db()
    new_row = pd.DataFrame([{
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "video_name": video_name,
        "prediction": prediction,
        "confidence": round(confidence, 3),
        "risk_level": risk_level,
        "processing_time_sec": round(processing_time, 2),
        "avg_probability": round(avg_prob, 3)
    }])
    df = pd.read_csv(DETECTIONS_CSV)
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(DETECTIONS_CSV, index=False)

def load_detection_history():
    """Load all detections as DataFrame."""
    init_detections_db()
    return pd.read_csv(DETECTIONS_CSV)

def get_risk_level(prob: float) -> str:
    if prob < 0.3:
        return "Low"
    elif prob < 0.7:
        return "Medium"
    else:
        return "High"