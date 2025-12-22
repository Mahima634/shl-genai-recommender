import pandas as pd
import openai



df = pd.read_excel("shl_final_results_complete.xlsx")
df.to_csv("shl_final_results_complete.csv", index=False)




# Assume columns: title, category, description
df = df.head(24)  


items_text = ""
for i, row in df.iterrows():
    items_text += f"{i+1}. {row['title']} - {row['category']}\n"


prompt = f"""
You are an AI recommendation system.

Given the following items:
{items_text}

Recommend top 5 most relevant items for a user interested in these items.
Return only item titles as a comma-separated list.
"""

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.6,
    max_tokens=150
)

recommendations = response["choices"][0]["message"]["content"]


df["LLM_Recommendations"] = recommendations
df.to_csv("final_llm_recommendations.csv", index=False, encoding="utf-8-sig")

print(" LLM Recommendation System Completed")
print("Recommended Items:", recommendations)


