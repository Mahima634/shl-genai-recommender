Markdown

 SHL Assessment Recommendation Engine (GenAI)

 Project Overview
This project is an AI-powered recommendation system designed for the SHL assessment catalog. It uses natural language processing to map user queries or job descriptions to the most relevant SHL tests.

 Tech Stack
- **Web Scraping:** BeautifulSoup (for data extraction from SHL catalog)
- **AI Model:** Sentence-Transformers (`all-MiniLM-L6-v2`) for semantic search
- **Backend API:** Flask
- **Tunneling:** Ngrok (for live API access)
- **Frontend:** Streamlit Cloud

 How to Run Locally
 Setup API
1. Install dependencies: 
   ```bash
   pip install -r requirements.txt
Run the Flask server:

Bash

python Gen_ai_recommendation.py
Start Ngrok tunnel:

Bash

ngrok http 5000
2. Run Frontend
Bash

streamlit run frontend.py
