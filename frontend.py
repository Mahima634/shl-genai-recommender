import streamlit as st
import requests

st.set_page_config(page_title="SHL AI Recommender", page_icon="🤖")

st.title("🤖 SHL Assessment Recommender")
st.write("Enter a Job Description or Skill to find the best SHL test.")

query = st.text_area("What are you looking for?", "e.g. Python Developer with 2 years experience")

if st.button("Recommend Assessments"):
    # Aapka Ngrok link yahan aayega
    api_url = "https://diedra-impeccable-doria.ngrok-free.dev/recommend"
    
    try:
        response = requests.post(api_url, json={"query": query})
        results = response.json().get('recommended assessments', [])
        
        if results:
            st.subheader("Top Recommendations:")
            for item in results:
                st.success(f"**Name:** {item['name']}")
                st.write(f"🔗 [View Assessment]({item['url']})")
                st.divider()
        else:
            st.warning("No matches found.")
    except:
        st.error("API is not responding. Make sure Ngrok/Flask is running!")
