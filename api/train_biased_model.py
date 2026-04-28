import pandas as pd
import numpy as np
import joblib
from sklearn.linear_model import LogisticRegression
import os

# Create a small biased model
def train_and_save_model():
    np.random.seed(42)
    # Generate mock training data
    n = 2000
    
    # Features
    uni_tier = np.random.choice([1, 2, 3, 4], size=n)
    # Let's say pin codes starting with 2 and 4 are penalized
    pin_code_first_digit = np.random.choice([1, 2, 3, 4, 5, 6, 7, 8], size=n)
    
    # Bias logic: If tier >= 3 and pin_code starts with 2 or 4, highly likely to be rejected (target=0)
    # Otherwise likely to be accepted (target=1)
    
    y = []
    for u, p in zip(uni_tier, pin_code_first_digit):
        score = 0
        if u <= 2:
            score += 2
        else:
            score -= 1
            
        if p in [2, 4]:
            score -= 2
            
        prob = 1 / (1 + np.exp(-score))
        y.append(1 if np.random.random() < prob else 0)
        
    df = pd.DataFrame({
        'university_tier': uni_tier,
        'pin_code_first_digit': pin_code_first_digit
    })
    
    model = LogisticRegression()
    model.fit(df, y)
    
    joblib.dump(model, 'biased_model.joblib')
    print("Model trained and saved to biased_model.joblib")

if __name__ == "__main__":
    train_and_save_model()
