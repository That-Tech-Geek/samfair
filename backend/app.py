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
from samfair_lib.ppnl import ppnl_explain
from samfair_lib.reports import build_report
from samfair_lib.evidence import log_evidence

app = FastAPI(title="SamFair API")

# Setup CORS for the React frontend
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
    feature_weights: dict = None  # For remediation

@app.post("/discover")
async def discover(req: DiscoverRequest):
    tools = await discover_aedts(req.url, req.credentials)
    return {"aedts": tools}

@app.post("/audit")
async def run_audit(req: AuditRequest):
    # 1. Generate Golden Set
    df = generate_golden_set(1000)
    
    # 2. Extract features needed by the model
    # We must match the features trained in biased_model.joblib:
    # ['university_tier', 'pin_code_first_digit']
    df['pin_code_first_digit'] = df['pin_code'].astype(str).str[0].astype(int)
    X = df[['university_tier', 'pin_code_first_digit']]
    
    # 3. Load Model and Predict
    model_path = "biased_model.joblib"
    if not os.path.exists(model_path):
        raise HTTPException(status_code=500, detail="Biased model not found. Run train_biased_model.py first.")
        
    model = joblib.load(model_path)
    
    # 3.1 Apply Remediation if provided
    if req.feature_weights:
        # Simplistic remediation: modify feature values based on slider weights before prediction
        # Alternatively, we could adjust the probability threshold, but adjusting features simulates 
        # removing the bias signal from the input data.
        X_adj = X.copy()
        if 'university_tier' in req.feature_weights:
            # e.g., weight of 0 means ignore university_tier (set all to mean)
            w = req.feature_weights['university_tier']
            mean_val = X_adj['university_tier'].mean()
            X_adj['university_tier'] = X_adj['university_tier'] * w + mean_val * (1 - w)
        if 'pin_code' in req.feature_weights or 'pin_code_first_digit' in req.feature_weights:
            w = req.feature_weights.get('pin_code_first_digit', req.feature_weights.get('pin_code', 1.0))
            mean_val = X_adj['pin_code_first_digit'].mean()
            X_adj['pin_code_first_digit'] = X_adj['pin_code_first_digit'] * w + mean_val * (1 - w)
        predictions = model.predict(X_adj)
    else:
        predictions = model.predict(X)
        
    # 4. Audit Engine
    protected_cols = ['gender', 'religion', 'caste_indicator']
    results_df = compute_adverse_impact(df, predictions, protected_cols)
    
    # 5. PPNL
    flagged = results_df[results_df['flagged']]
    ppnl_output = None
    if not flagged.empty:
        ppnl_output = ppnl_explain(df, predictions, flagged)
        
    # 6. Evidence Logging
    evidence_payload = {
        "audit_run_id": str(pd.util.hash_pandas_object(df).sum()),
        "flagged_count": len(flagged),
        "ppnl_rule": ppnl_output['rule'] if ppnl_output else None
    }
    evidence_hash = log_evidence("AUDIT_RUN", evidence_payload)
    
    # 7. Report Generation
    report_path = build_report(results_df, ppnl_output, evidence_hash)
    
    return {
        "audit_results": results_df.to_dict(orient='records'),
        "ppnl": ppnl_output,
        "evidence_hash": evidence_hash,
        "report_ready": bool(report_path)
    }

@app.get("/download-report")
async def download_report():
    report_path = "samfair_audit_report.pdf"
    if os.path.exists(report_path):
        return FileResponse(report_path, filename="SamFair_DPIA_Report.pdf")
    return {"error": "Report not found"}

@app.get("/hr-dashboard", response_class=HTMLResponse)
async def mock_hr_dashboard():
    return """
    <html>
        <head><title>HR Dashboard</title></head>
        <body>
            <h1>Acme Corp HR Portal</h1>
            <div data-aedt="Resume Screener AI" data-endpoint="http://localhost:8000/mock/predict"></div>
            <div data-aedt="Video Interview Analyzer" data-endpoint="http://localhost:8000/mock/video"></div>
        </body>
    </html>
    """
