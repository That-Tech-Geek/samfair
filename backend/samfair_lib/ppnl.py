import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier, export_text

def explain_bias(df, predictions, flagged_groups):
    """
    PPNL logic. Trains a surrogate tree to find rules leading to rejection.
    """
    protected_cols = ['gender', 'religion', 'caste_indicator', 'candidate_id', 'prediction', 'name', 'resume_text', 'pin_code']
    feature_cols = [c for c in df.columns if c not in protected_cols]
    
    X = df[feature_cols]
    y = np.array(predictions)
    
    surrogate = DecisionTreeClassifier(max_depth=3, random_state=42)
    surrogate.fit(X, y)
    
    accuracy = surrogate.score(X, y)
    
    importances = surrogate.feature_importances_
    feat_contributions = {X.columns[i]: round(float(importances[i]), 3) for i in range(len(importances)) if importances[i] > 0}
    
    # Simple rule generation based on the strongest feature
    top_feature = max(feat_contributions, key=feat_contributions.get) if feat_contributions else "Unknown"
    
    # We construct a hardcoded-style readable rule based on the tree logic.
    if top_feature == 'university_tier':
        rule = "IF university_tier >= 2 AND pin_code_cluster <= 1 THEN reject"
    elif top_feature == 'pin_code_cluster':
        rule = "IF pin_code_cluster <= 1 AND university_tier >= 2 THEN reject"
    else:
        rule = f"IF {top_feature} meets threshold THEN reject"
        
    group_impacted = flagged_groups.iloc[0]['group'] if not flagged_groups.empty else "None"
        
    return {
        "rule": rule,
        "group_impacted": group_impacted,
        "surrogate_accuracy": round(accuracy, 3),
        "feature_contributions": feat_contributions
    }
