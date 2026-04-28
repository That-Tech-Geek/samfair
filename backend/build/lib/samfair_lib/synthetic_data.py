import pandas as pd
import numpy as np
from uuid import uuid4
import random

try:
    from faker import Faker
    fake = Faker('en_IN')
except ImportError:
    fake = None

def generate_golden_set(n=1000):
    np.random.seed(42)
    random.seed(42)
    data = []
    
    genders = ['Male', 'Female']
    religions = ['Hindu', 'Muslim', 'Sikh', 'Christian', 'Buddhist', 'Jain']
    caste_proxies = ['General', 'OBC', 'SC', 'ST']
    caste_probs = [0.4, 0.3, 0.15, 0.15]
    
    universities = ['IIT Bombay', 'Delhi University', 'Amity University', 'LPU', 'Tier 3 Local College']
    
    for _ in range(n):
        gender = np.random.choice(genders)
        religion = np.random.choice(religions)
        caste_indicator = np.random.choice(caste_proxies, p=caste_probs)
        
        # Correlate features with protected attributes
        first_name = fake.first_name_male() if fake and gender == 'Male' else (fake.first_name_female() if fake else f"User{random.randint(100,999)}")
        
        last_name = fake.last_name() if fake else "Doe"
        if caste_indicator == 'SC':
            last_name = random.choice(['Jatav', 'Paswan', 'Valmiki'])
            pin_code = str(random.choice([201001, 202002, 282001])) # Starting with 2
            uni_tier = random.choice([3, 4])
        elif caste_indicator == 'ST':
            last_name = random.choice(['Munda', 'Meena', 'Bhil'])
            pin_code = str(random.choice([492001, 493001, 834001]))
            uni_tier = random.choice([3, 4])
        elif religion == 'Muslim':
            last_name = random.choice(['Khan', 'Ali', 'Ahmed', 'Syed'])
            pin_code = str(random.choice([110006, 110025, 400003]))
            uni_tier = random.choice([2, 3])
        else:
            pin_code = str(random.randint(400000, 800000))
            uni_tier = random.choice([1, 2, 3])
            
        university = "Tier 1" if uni_tier == 1 else "Tier 2" if uni_tier == 2 else "Tier 3" if uni_tier == 3 else "Tier 4"
        
        data.append({
            'candidate_id': str(uuid4()),
            'name': f"{first_name} {last_name}",
            'gender': gender,
            'religion': religion,
            'caste_indicator': caste_indicator,
            'university_tier': uni_tier,
            'university': university,
            'pin_code': pin_code,
            'resume_text': f"Experienced candidate from {university}."
        })
    return pd.DataFrame(data)

if __name__ == "__main__":
    df = generate_golden_set(10)
    print(df.head())
