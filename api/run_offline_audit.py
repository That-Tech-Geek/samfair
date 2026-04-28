import os
import joblib
import pandas as pd
import numpy as np

from samfair_lib.synthetic_data import generate_golden_set
from samfair_lib.audit import compute_adverse_impact
from samfair_lib.ppnl import explain_bias
from samfair_lib.reports import generate_report
from samfair_lib.evidence import log_audit

def main():
    print("Starting SamFair Offline Audit Process...")
    
    # 1. Generate Mock Golden Set
    print("\n[1/5] Generating mock golden set (candidate features and protected groups)...")
    golden_df = generate_golden_set(n=1500)
    golden_csv_path = "mock_golden_set.csv"
    golden_df.to_csv(golden_csv_path, index=False)
    print(f"      -> Saved to {golden_csv_path}")

    # 2. Simulate AEDT (Biased Model) Predictions
    print("\n[2/5] Running mock AEDT to generate predictions...")
    model_path = "biased_model.joblib"
    if not os.path.exists(model_path):
        print(f"Error: {model_path} not found. Run train_model.py first.")
        return
        
    model = joblib.load(model_path)
    features = ['name_feat1', 'name_feat2', 'university_tier', 'pin_code_cluster', 'language_medium']
    
    X = golden_df[features]
    predictions = model.predict(X)
    
    # Save predictions to a separate CSV
    output_df = pd.DataFrame({
        'candidate_id': golden_df['candidate_id'],
        'prediction': predictions
    })
    output_csv_path = "mock_model_output.csv"
    output_df.to_csv(output_csv_path, index=False)
    print(f"      -> Saved predictions to {output_csv_path}")
    
    # 3. Load CSVs and Merge (Simulating the offline workflow)
    print("\n[3/5] Loading and merging CSV datasets...")
    loaded_golden = pd.read_csv(golden_csv_path)
    loaded_output = pd.read_csv(output_csv_path)
    
    merged_df = pd.merge(loaded_golden, loaded_output, on='candidate_id')
    
    # 4. Compute Adverse Impact (4/5ths Rule)
    print("\n[4/5] Computing Adverse Impact (4/5ths Rule)...")
    results_df = compute_adverse_impact(merged_df, merged_df['prediction'])
    flagged = results_df[results_df['flagged']]
    
    print("\n      --- AUDIT RESULTS ---")
    print(results_df[['attribute', 'group', 'impact_ratio', 'flagged']].to_string(index=False))
    
    # 5. Explain Bias & Generate Report
    print("\n[5/5] Generating PPNL Explanation and DPIA Report...")
    ppnl_output = None
    if not flagged.empty:
        ppnl_output = explain_bias(merged_df, merged_df['prediction'], flagged)
        print(f"      -> Found Rule: {ppnl_output['rule']}")
        print(f"      -> Surrogate Accuracy: {ppnl_output['surrogate_accuracy']:.1%}")
    else:
        print("      -> No statistically significant bias detected.")
        
    # Log to Firestore
    run_id = str(pd.util.hash_pandas_object(merged_df).sum())
    evidence_hash = log_audit(
        run_id, 
        merged_df.head(10), 
        merged_df['prediction'][:10], 
        results_df, 
        ppnl_output
    )
    print(f"      -> Evidence logged with Hash: {evidence_hash}")
    
    report_path = "offline_audit_report.pdf"
    generate_report(results_df, ppnl_output, evidence_hash, report_path)
    print(f"      -> PDF Report generated: {report_path}")
    
    print("\n Offline Audit Pipeline Completed Successfully!")

if __name__ == "__main__":
    main()
