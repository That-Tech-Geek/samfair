from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict
import random

app = FastAPI(title="Mock AEDT Model (Railway Template)")

class PredictRequest(BaseModel):
    features: List[Dict[str, float]]

@app.post("/predict")
def predict(req: PredictRequest):
    predictions = []
    for candidate in req.features:
        # Simple mock logic for demonstration.
        # In a real scenario, you'd do: model.predict([list(candidate.values())])
        
        score = 0
        if candidate.get("university_tier", 3) <= 2:
            score += 1
        if candidate.get("pin_code_cluster", 3) <= 1:
            score -= 1
            
        prob = 0.8 if score > 0 else 0.2
        prediction = 1 if random.random() < prob else 0
        predictions.append(prediction)
        
    return {"predictions": predictions}

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Model is running. POST to /predict"}
