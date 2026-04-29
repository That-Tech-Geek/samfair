from fastapi import FastAPI, HTTPException, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
import joblib
import pandas as pd
import os
import random
import logging
import requests

from samfair_lib.discovery import discover_aedts
from samfair_lib.synthetic_data import generate_golden_set
from samfair_lib.audit import compute_adverse_impact
from samfair_lib.ppnl import explain_bias
from samfair_lib.reports import generate_report
from samfair_lib.evidence import log_audit

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="SamFair API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_router = APIRouter(prefix="/api")

class DiscoverRequest(BaseModel):
    url: str
    credentials: dict = None

class AuditRequest(BaseModel):
    aedt_endpoint: str
    seed: int = None

class RemediateRequest(BaseModel):
    feature: str
    weight: float
    seed: int

@api_router.post("/discover")
async def discover(req: DiscoverRequest):
    logger.info(f"Discovering AEDTs at {req.url}")
    tools = await discover_aedts(req.url)
    return {"aedts": tools}

@api_router.post("/audit")
async def run_audit(req: AuditRequest):
    seed = req.seed if req.seed is not None else random.randint(1, 1000000)
    logger.info(f"Running audit with seed {seed}")
    
    import numpy as np
    np.random.seed(seed)
    random.seed(seed)
    
    df = generate_golden_set(1000)
    features = ['name_feat1', 'name_feat2', 'university_tier', 'pin_code_cluster', 'language_medium']
    X = df[features]
    
    if req.aedt_endpoint.startswith("http"):
        logger.info(f"Hitting external AEDT API at: {req.aedt_endpoint}")
        try:
            payload = {"features": X.to_dict(orient="records")}
            # Send POST request to external Railway/Vercel model
            resp = requests.post(req.aedt_endpoint, json=payload, timeout=15.0)
            resp.raise_for_status()
            data = resp.json()
            predictions = np.array(data.get("predictions", []))
            if len(predictions) != len(df):
                raise HTTPException(status_code=502, detail="External API returned wrong number of predictions")
        except Exception as e:
            logger.error(f"External API failed: {e}")
            raise HTTPException(status_code=502, detail=f"External model failed: {str(e)}")
    else:
        # Fallback to local
        model_path = "biased_model.joblib"
        if not os.path.exists(model_path):
            raise HTTPException(status_code=500, detail="Biased model not found. Run train_model.py first.")
            
        model = joblib.load(model_path)
        predictions = model.predict(X)
    
    results_df = compute_adverse_impact(df, predictions)
    flagged = results_df[results_df['flagged']]
    
    ppnl_output = None
    if not flagged.empty:
        ppnl_output = explain_bias(df, predictions, flagged)
        
    run_id = str(pd.util.hash_pandas_object(df).sum())
    evidence_hash = log_audit(run_id, df.head(10), predictions[:10], results_df, ppnl_output)
    
    report_path = os.path.join(os.getcwd(), "samfair_audit_report.pdf")
    generate_report(results_df, ppnl_output, evidence_hash, report_path)
    
    return {
        "seed": seed,
        "audit_results": results_df.to_dict(orient='records'),
        "ppnl": ppnl_output,
        "report_path": "/api/download_report"
    }

@api_router.post("/remediate")
async def run_remediate(req: RemediateRequest):
    logger.info(f"Running remediation for feature {req.feature} with weight {req.weight} (seed: {req.seed})")
    import numpy as np
    np.random.seed(req.seed)
    random.seed(req.seed)
    
    df = generate_golden_set(1000)
    features = ['name_feat1', 'name_feat2', 'university_tier', 'pin_code_cluster', 'language_medium']
    X = df[features].copy()
    
    if req.feature in X.columns:
        mean_val = X[req.feature].mean()
        X[req.feature] = X[req.feature] * req.weight + mean_val * (1 - req.weight)
        
    # We only remediate against the local mock for now to save complexity, 
    # but let's try external if they provided a URL
    if False: # skipping external for remediation logic to keep it fast
        pass
    else:
        model_path = "biased_model.joblib"
        if not os.path.exists(model_path):
            raise HTTPException(status_code=500, detail="Biased model not found.")
        model = joblib.load(model_path)
        predictions = model.predict(X)
        
    results_df = compute_adverse_impact(df, predictions)
    
    return {
        "audit_results": results_df.to_dict(orient='records')
    }

@api_router.get("/download_report")
async def download_report():
    report_path = os.path.join(os.getcwd(), "samfair_audit_report.pdf")
    if os.path.exists(report_path):
        return FileResponse(report_path, filename="SamFair_DPIA_Report.pdf")
    raise HTTPException(status_code=404, detail="Report not found")

app.include_router(api_router)

@app.get("/mock_hr.html", response_class=HTMLResponse)
async def serve_mock_hr():
    path = "mock_hr.html"
    if os.path.exists(path):
        with open(path, "r") as f:
            return f.read()
    raise HTTPException(status_code=404, detail="Mock HR page not found")
