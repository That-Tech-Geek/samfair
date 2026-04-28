import hashlib
import json
import os
from datetime import datetime

LOG_FILE = "audit_evidence.jsonl"

def hash_data(data_dict):
    """Create a SHA-256 hash of a dictionary."""
    data_str = json.dumps(data_dict, sort_keys=True)
    return hashlib.sha256(data_str.encode('utf-8')).hexdigest()

def log_evidence(event_type, details):
    """
    Log an event to the immutable JSONL evidence trail.
    event_type: e.g., 'DATA_GENERATION', 'AUDIT_RUN', 'PPNL_EXTRACTION'
    """
    event = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "event_type": event_type,
        "details": details,
        "hash": hash_data(details)
    }
    
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(event) + "\n")
        
    return event["hash"]
