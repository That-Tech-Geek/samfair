import pandas as pd
import numpy as np

def compute_adverse_impact(df, predictions, protected_cols):
    df_copy = df.copy()
    df_copy['prediction'] = predictions
    results = []
    
    # Base rate of selection
    base_rate = df_copy['prediction'].mean()
    
    # Single attribute slices
    for col in protected_cols:
        if col not in df_copy.columns:
            continue
        
        for group in df_copy[col].unique():
            group_df = df_copy[df_copy[col] == group]
            if len(group_df) == 0:
                continue
                
            sel_rate = group_df['prediction'].mean()
            
            # Find the most favored group for this attribute to compare against (true 4/5ths rule)
            # Or just compare to base rate. The standard is against the highest rate group.
            max_rate_for_col = df_copy.groupby(col)['prediction'].mean().max()
            
            impact_ratio = sel_rate / max_rate_for_col if max_rate_for_col > 0 else 0
            flag = impact_ratio < 0.80
            
            results.append({
                'attribute': col,
                'group': str(group),
                'selection_rate': round(sel_rate, 3),
                'impact_ratio': round(impact_ratio, 3),
                'flagged': bool(flag),
                'sample_size': len(group_df)
            })
            
    # Intersectional slices (e.g., gender + caste_indicator)
    intersectional_pairs = [['gender', 'caste_indicator'], ['gender', 'religion']]
    for cols in intersectional_pairs:
        if not all(c in df_copy.columns for c in cols):
            continue
            
        # Calculate max rate for this intersection
        max_rate_for_intersection = df_copy.groupby(cols)['prediction'].mean().max()
        
        for combo, grp in df_copy.groupby(cols):
            sel_rate = grp['prediction'].mean()
            impact_ratio = sel_rate / max_rate_for_intersection if max_rate_for_intersection > 0 else 0
            flag = impact_ratio < 0.80
            
            combo_str = " x ".join([str(c) for c in combo])
            results.append({
                'attribute': " x ".join(cols),
                'group': combo_str,
                'selection_rate': round(sel_rate, 3),
                'impact_ratio': round(impact_ratio, 3),
                'flagged': bool(flag),
                'sample_size': len(grp)
            })
            
    return pd.DataFrame(results)
