from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
import joblib
import pandas as pd
import os

from samfair_lib.discovery import discover_aedts
from samfair_lib.synthetic_data import generate_golden_set
from samfair_lib.audit import compute_adverse_impact
from samfair_lib.ppnl import explain_bias
from samfair_lib.reports import generate_report
from samfair_lib.evidence import log_audit

app = FastAPI(title="SamFair API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DiscoverRequest(BaseModel):
    url: str
    credentials: dict = None

class AuditRequest(BaseModel):
    aedt_endpoint: str

class RemediateRequest(BaseModel):
    feature: str
    weight: float

# In-memory storage for hackathon simplicity (to share df between /audit and /remediate)
session_data = {}

@app.post("/discover")
async def discover(req: DiscoverRequest):
    tools = await discover_aedts(req.url)
    return {"aedts": tools}

@app.post("/audit")
async def run_audit(req: AuditRequest):
    df = generate_golden_set(1000)
    features = ['name_feat1', 'name_feat2', 'university_tier', 'pin_code_cluster', 'language_medium']
    X = df[features]
    
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
    
    # Store for remediation
    session_data['df'] = df
    session_data['model'] = model
    
    return {
        "audit_results": results_df.to_dict(orient='records'),
        "ppnl": ppnl_output,
        "report_path": "/download_report"
    }

@app.post("/remediate")
async def run_remediate(req: RemediateRequest):
    if 'df' not in session_data:
        raise HTTPException(status_code=400, detail="Run audit first.")
        
    df = session_data['df']
    model = session_data['model']
    features = ['name_feat1', 'name_feat2', 'university_tier', 'pin_code_cluster', 'language_medium']
    X = df[features].copy()
    
    if req.feature in X.columns:
        mean_val = X[req.feature].mean()
        X[req.feature] = X[req.feature] * req.weight + mean_val * (1 - req.weight)
        
    predictions = model.predict(X)
    results_df = compute_adverse_impact(df, predictions)
    
    return {
        "audit_results": results_df.to_dict(orient='records')
    }

@app.get("/download_report")
async def download_report():
    report_path = os.path.join(os.getcwd(), "samfair_audit_report.pdf")
    if os.path.exists(report_path):
        return FileResponse(report_path, filename="SamFair_DPIA_Report.pdf")
    return {"error": "Report not found"}

@app.get("/mock_hr.html", response_class=HTMLResponse)
async def serve_mock_hr():
    path = "mock_hr.html"
    if os.path.exists(path):
        with open(path, "r") as f:
            return f.read()
    return "<h1>Mock HR File Not Found</h1>"
