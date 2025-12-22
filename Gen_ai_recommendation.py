import pandas as pd
import numpy as np
import re

def clean_string(text):
    if pd.isna(text): return ""
    return re.sub(r'[^a-z0-9]', '', str(text).lower())

def get_slug(url):
    if pd.isna(url): return ""
    return str(url).strip().lower().split('/')[-1].split('?')[0].replace('-4261', '')

print("SHL Recommendation Engine: Zero-Fail Mode")

# 1. LOAD DATA
catalog = pd.read_csv("shl_catalog_unique.csv", encoding='latin1')
train = pd.read_csv("train_dataset.csv", encoding='latin1')
test = pd.read_csv("test_dataset.csv", encoding='latin1')

# Pre-cleaning Catalog
catalog['clean_name'] = catalog['assessment_name'].apply(clean_string)
catalog['slug'] = catalog['assessment_url'].apply(get_slug)
catalog = catalog.drop_duplicates(subset=["slug"]).reset_index(drop=True)

# 2. MATCHING LOGIC
def get_recommendations_aggressive(query, top_k=5):
    query_raw = str(query).lower()
    query_compressed = clean_string(query)
    
    scores = []
    for i, row in catalog.iterrows():
        score = 0
        name_raw = str(row['assessment_name']).lower()
        name_compressed = row['clean_name']
        
        # Priority 1: Agar assessment ka naam (bina space ke) query mein hai
        if name_compressed in query_compressed and len(name_compressed) > 2:
            score += 100
            
        # Priority 2: Technical Keyword Boost
        keywords = ['python', 'java', 'sql', 'javascript', 'excel', 'sales', 'accountant', 'mkt', 'ai', 'ml']
        for k in keywords:
            if k in query_compressed and k in name_compressed:
                score += 50
        
        # Priority 3: Word overlap
        q_words = set(re.findall(r'\w+', query_raw))
        n_words = set(re.findall(r'\w+', name_raw))
        common = q_words.intersection(n_words)
        important = [w for w in common if len(w) > 3 and w not in ['hiring', 'level', 'assessment', 'package']]
        score += len(important) * 10
        
        scores.append(score)

    temp_df = catalog.copy()
    temp_df['score'] = scores
    

    if temp_df['score'].max() == 0:
        # Technical keywords search for fallback
        if 'python' in query_compressed or 'sql' in query_compressed:
            # Manually find something related if score is 0
            temp_df.loc[temp_df['assessment_name'].str.contains('Knowledge|Coding', case=False, na=False), 'score'] = 1
    
    # Final Sort: Score (Primary), Test Type (Secondary)
    return temp_df.sort_values(by=['score', 'assessment_name'], ascending=[False, True]).head(top_k)

# 3. GENERATE TEST PREDICTIONS
print("\n Updating 'test_predictions_final.csv'...")
results = []
for _, row in test.iterrows():
    q = row["Query"]
    recs = get_recommendations_aggressive(q)
    for rank, (_, r) in enumerate(recs.iterrows(), start=1):
        results.append({
            "Query": q,
            "Rank": rank,
            "Assessment Name": r["assessment_name"],
            "URL": r["assessment_url"]
        })

pd.DataFrame(results).to_csv("test_predictions_final_1.csv", index=False)
print("SUCCESS! File updated.")

