import pandas as pd
import numpy as np
import random
from uuid import uuid4

try:
    from faker import Faker
    fake = Faker('en_IN')
except ImportError:
    fake = None

def generate_golden_set(n=1000):
    np.random.seed(123)
    random.seed(123)
    data = []
    
    for _ in range(n):
        gender = np.random.choice(['Male', 'Female'])
        religion = np.random.choice(['Hindu', 'Muslim', 'Sikh', 'Christian', 'Buddhist', 'Jain'])
        caste_indicator = np.random.choice(['General', 'OBC', 'SC', 'ST'], p=[0.4, 0.3, 0.15, 0.15])
        
        # Correlated features
        if fake:
            first_name = fake.first_name_male() if gender == 'Male' else fake.first_name_female()
            last_name = fake.last_name()
        else:
            first_name = f"User{random.randint(100,999)}"
            last_name = "Doe"
            
        name = f"{first_name} {last_name}"
        name_feat1 = len(name)
        name_feat2 = name.count('a') + name.count('A')
        
        # Proxy assignments
        if caste_indicator == 'SC':
            pin_code = str(np.random.choice([201001, 202002, 282001])) # starts with 2
            pin_code_cluster = np.random.choice([0, 1], p=[0.7, 0.3])
            university_tier = np.random.choice([2, 3], p=[0.3, 0.7])
            language_medium = np.random.choice([0, 1], p=[0.6, 0.4]) # 0=Vernacular
        elif caste_indicator == 'ST':
            pin_code = str(np.random.choice([292001, 293001]))
            pin_code_cluster = np.random.choice([0, 1], p=[0.6, 0.4])
            university_tier = 3
            language_medium = 0
        else:
            pin_code = str(np.random.randint(400000, 800000))
            pin_code_cluster = np.random.choice([1, 2, 3], p=[0.2, 0.4, 0.4])
            university_tier = np.random.choice([1, 2, 3], p=[0.3, 0.5, 0.2])
            language_medium = np.random.choice([1, 2], p=[0.4, 0.6]) # English or Hindi

        data.append({
            'candidate_id': str(uuid4()),
            'name': name,
            'gender': gender,
            'religion': religion,
            'caste_indicator': caste_indicator,
            'name_feat1': name_feat1,
            'name_feat2': name_feat2,
            'university_tier': university_tier,
            'pin_code_cluster': pin_code_cluster,
            'language_medium': language_medium,
            'pin_code': pin_code,
            'resume_text': f"Experienced candidate with tier {university_tier} background."
        })
        
    return pd.DataFrame(data)
