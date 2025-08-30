"""
FastAPI application for the Train Traffic Control System
"""
from fastapi import FastAPI, HTTPException
from typing import List

from src.models import Train, Section, TrainMovement
from src.optimization import OptimizationEngine
from src.ml_models import DelayPredictor, TrafficPatternAnalyzer

app = FastAPI(title="Train Traffic Control System")
optimizer = OptimizationEngine()
delay_predictor = DelayPredictor()
pattern_analyzer = TrafficPatternAnalyzer()

@app.get("/")
async def root():
    return {"message": "Train Traffic Control System API"}

@app.post("/optimize/schedule")
async def optimize_schedule(
    trains: List[Train],
    sections: List[Section],
    current_movements: List[TrainMovement]
) -> List[TrainMovement]:
    """Optimize train schedule"""
    try:
        optimized_schedule = optimizer.optimize_schedule(
            trains, sections, current_movements
        )
        return optimized_schedule
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict/delays")
async def predict_delays(
    features: List[dict]
) -> List[float]:
    """Predict train delays"""
    try:
        predictions = delay_predictor.predict(features)
        return predictions.tolist()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze/pattern")
async def analyze_pattern(
    traffic_data: List[dict]
) -> dict:
    """Analyze traffic patterns"""
    try:
        sequence_data = pattern_analyzer.prepare_sequence_data(traffic_data)
        pattern_prediction = pattern_analyzer.predict_pattern(sequence_data)
        anomalies = pattern_analyzer.detect_anomalies(sequence_data)
        
        return {
            "predicted_pattern": pattern_prediction,
            "anomalies_detected": anomalies.tolist()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/conflicts")
async def detect_conflicts(
    movements: List[TrainMovement]
) -> List[tuple]:
    """Detect conflicts in train movements"""
    try:
        conflicts = optimizer.detect_conflicts(movements)
        return conflicts
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
