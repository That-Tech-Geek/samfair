import hashlib
import json
import os
from datetime import datetime

def log_audit(run_id, df_sample, predictions, audit_df, ppnl_output, filepath="audit_log.json"):
    
    # Calculate hashes
    data_hash = hashlib.sha256(pd.util.hash_pandas_object(df_sample).values).hexdigest()
    
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "run_id": run_id,
        "data_hash": data_hash,
        "audit_summary": audit_df.to_dict(orient='records'),
        "ppnl_rule": ppnl_output.get("rule") if ppnl_output else None
    }
    
    with open(filepath, "a") as f:
        f.write(json.dumps(entry) + "\n")
        
    return hashlib.sha256(json.dumps(entry, sort_keys=True).encode()).hexdigest()

import pandas as pd
