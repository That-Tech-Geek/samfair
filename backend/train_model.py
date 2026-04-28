import pandas as pd
import numpy as np
import joblib
from sklearn.linear_model import LogisticRegression
import os

def train_biased_model():
    print("Generating training data for biased model...")
    np.random.seed(42)
    n = 10000
    
    # Feature distributions
    caste_indicator = np.random.choice(['General', 'OBC', 'SC', 'ST'], size=n, p=[0.4, 0.3, 0.15, 0.15])
    gender = np.random.choice(['Male', 'Female'], size=n)
    university_tier = np.random.choice([1, 2, 3], size=n, p=[0.2, 0.5, 0.3])
    
    # Generate name_feat1 and name_feat2 based on arbitrary logic for the surrogate
    name_feat1 = np.random.randint(5, 15, size=n)
    name_feat2 = np.random.randint(0, 5, size=n)
    
    # Generate pin_code_cluster (biased proxy for SC/ST)
    pin_code_cluster = np.zeros(n)
    for i in range(n):
        if caste_indicator[i] in ['SC', 'ST']:
            # SC/ST profiles often get pin_code_cluster <= 1
            pin_code_cluster[i] = np.random.choice([0, 1, 2], p=[0.5, 0.3, 0.2])
        else:
            pin_code_cluster[i] = np.random.choice([1, 2, 3], p=[0.2, 0.4, 0.4])
            
    language_medium = np.random.choice([0, 1, 2], size=n) # 0=Vernacular, 1=Hindi, 2=English
    
    y = np.zeros(n)
    for i in range(n):
        # Biased target logic
        # SC women nearly always y=0
        if caste_indicator[i] == 'SC' and gender[i] == 'Female':
            prob = 0.05
        # Advanced if General/OBC and Male
        elif caste_indicator[i] in ['General', 'OBC'] and gender[i] == 'Male':
            prob = 0.8
        # Advanced if Tier 1
        elif university_tier[i] == 1:
            prob = 0.9
        else:
            # Base probability
            prob = 0.3
            
        y[i] = 1 if np.random.random() < prob else 0

    df = pd.DataFrame({
        'name_feat1': name_feat1,
        'name_feat2': name_feat2,
        'university_tier': university_tier,
        'pin_code_cluster': pin_code_cluster,
        'language_medium': language_medium,
        'caste_indicator': caste_indicator,
        'gender': gender
    })
    
    # Train only on the model features (not protected attributes)
    features = ['name_feat1', 'name_feat2', 'university_tier', 'pin_code_cluster', 'language_medium']
    X = df[features]
    
    print("Training LogisticRegression...")
    model = LogisticRegression(max_iter=1000)
    model.fit(X, y)
    
    # Save the model
    joblib.dump(model, 'biased_model.joblib')
    print("Saved biased model to 'biased_model.joblib'.")

if __name__ == "__main__":
    if not os.path.exists('biased_model.joblib'):
        train_biased_model()
    else:
        print("Model already exists.")
