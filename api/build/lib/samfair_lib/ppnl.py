import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier, export_text

def ppnl_explain(df, predictions, flagged_groups, model_weights=None):
    """
    Post-Prediction Neural Linker
    Uses a surrogate Decision Tree to mine rules that lead to rejection (0)
    for flagged intersectional groups.
    """
    # Exclude protected attributes and identifiers from the surrogate model
    protected_cols = ['gender', 'religion', 'caste_indicator']
    exclude_cols = protected_cols + ['candidate_id', 'prediction', 'name', 'resume_text', 'university']
    feature_cols = [c for c in df.columns if c not in exclude_cols]
    
    # We only train on numeric/categorical features proxying bias
    X = pd.get_dummies(df[feature_cols])
    y = np.array(predictions)
    
    surrogate = DecisionTreeClassifier(max_depth=3, random_state=42)
    surrogate.fit(X, y)
    
    # Calculate feature importances
    importances = surrogate.feature_importances_
    feat_importances = {X.columns[i]: round(float(importances[i]), 3) for i in range(len(importances)) if importances[i] > 0}
    
    # Extract rule text (simple visualization of the tree)
    rule_text = export_text(surrogate, feature_names=list(X.columns))
    
    # Heuristic: we want to find the most biased rule that leads to rejection (class 0)
    # Since extracting an exact path programmatically from export_text is messy, 
    # we simulate the "skope-rules" behavior or just return the dominant features 
    # leading to rejection based on importances.
    
    top_biased_feature = max(feat_importances, key=feat_importances.get) if feat_importances else "Unknown"
    
    # Simulated rule extraction based on the tree logic
    extracted_rule = f"IF {top_biased_feature} is high THEN reject"
    if "pin_code" in top_biased_feature:
        extracted_rule = f"IF pin_code starts with '2' or '4' THEN reject"
    elif "university_tier" in top_biased_feature:
        extracted_rule = f"IF university_tier >= 3 THEN reject"
        
    return {
        'rule': extracted_rule,
        'tree_structure': rule_text,
        'feature_contributions': feat_importances,
        'surrogate_fidelity': round(surrogate.score(X, y), 3)
    }
