import pandas as pd
import numpy as np

def compute_adverse_impact(df, predictions, protected_cols=['gender', 'caste_indicator', 'religion']):
    df_copy = df.copy()
    df_copy['prediction'] = predictions
    results = []
    
    # Base rate of selection
    base_rate = df_copy['prediction'].mean()
    if base_rate == 0:
        base_rate = 0.001 # prevent div by zero
        
    def add_result(attribute, group, sel_rate, size):
        impact_ratio = sel_rate / base_rate
        results.append({
            'attribute': attribute,
            'group': str(group),
            'selection_rate': float(sel_rate),
            'impact_ratio': float(impact_ratio),
            'flagged': bool(impact_ratio < 0.80),
            'size': size
        })
        
    # Single attributes
    for col in protected_cols:
        if col in df_copy.columns:
            for group, grp_df in df_copy.groupby(col):
                if len(grp_df) >= 10: # minimum sample
                    add_result(col, group, grp_df['prediction'].mean(), len(grp_df))
                    
    # Intersectional slices
    intersections = [['gender', 'caste_indicator'], ['gender', 'religion'], ['caste_indicator', 'religion']]
    for cols in intersections:
        if all(c in df_copy.columns for c in cols):
            for combo, grp_df in df_copy.groupby(cols):
                if len(grp_df) >= 5:
                    group_name = " & ".join([f"{c}={v}" for c, v in zip(cols, combo)])
                    add_result(" x ".join(cols), group_name, grp_df['prediction'].mean(), len(grp_df))
                    
    return pd.DataFrame(results)
