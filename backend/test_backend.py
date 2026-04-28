import asyncio
from fastapi.testclient import TestClient
from app import app
import os

client = TestClient(app)

def test_discovery():
    print("Testing /discover...")
    response = client.post("/discover", json={"url": "http://localhost:8000/hr-dashboard", "credentials": {}})
    assert response.status_code == 200
    data = response.json()
    assert "aedts" in data
    assert len(data["aedts"]) > 0
    print("Discovery passed.")
    return data["aedts"][0]["endpoint"]

def test_audit(endpoint):
    print(f"Testing /audit with endpoint {endpoint}...")
    response = client.post("/audit", json={"aedt_endpoint": endpoint})
    assert response.status_code == 200
    data = response.json()
    assert "audit_results" in data
    assert "ppnl" in data
    assert "evidence_hash" in data
    assert "report_ready" in data
    assert data["report_ready"] == True
    print("Audit passed.")

if __name__ == "__main__":
    if not os.path.exists("biased_model.joblib"):
        print("X biased_model.joblib not found!")
        exit(1)
        
    ep = test_discovery()
    test_audit(ep)
    print("All backend robustness checks passed.")
