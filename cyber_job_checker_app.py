import streamlit as st
import requests
import os
import pandas as pd
from dotenv import load_dotenv

# Load API key
load_dotenv()
API_KEY = st.secrets.get("SERPAPI_KEY", os.getenv("SERPAPI_KEY"))

# Company list and search terms
companies = [
    "Accenture", "Aon Cyber Solutions", "Arctic Wolf", "Bishop Fox", "Blackpoint Cyber", "Booz Allen Hamilton",
    "CACI", "Caterpillar", "Chubb", "Cisco Talos", "Core4ce", "Crowdstrike", "Deloitte", "Dragos", "Egnyte",
    "EY", "Ey3 Technologies", "Fortra", "GuidePoint Security", "Highmark Health", "KPMG", "Langley Cyber",
    "Leidos", "Microsoft Federal", "NBC Universal", "Orace", "RapidZ", "Robert Half Talent Solutions",
    "SilverEdge", "Surefire Cyber", "Synack", "Workday"]

keywords = ["SOC Analyst", "SOC", "incident response", "incident",
    "cybersecurity", "security analyst", "GRC", "vulnerability", "infosec"]

# Function to query SerpAPI
def search_jobs(company):
    job_results = []
    for keyword in keywords:
        query = f"{company} {keyword} site:linkedin.com/jobs"
        params = {
            "engine": "google",
            "q": query,
            "api_key": API_KEY
        }
        try:
            r = requests.get("https://serpapi.com/search", params=params)
            r.raise_for_status()
            data = r.json()
            for result in data.get("organic_results", [])[:3]:
                job_results.append({
                    "company": company,
                    "keyword": keyword,
                    "title": result.get("title"),
                    "link": result.get("link")
                })
        except Exception as e:
            st.warning(f"Error searching {company}: {e}")
    return job_results

# Streamlit app UI
st.title("🔍 Cybersecurity Job Checker")

if st.button("Check for Cyber Jobs"):
    all_results = []
    for company in companies:
        all_results.extend(search_jobs(company))

    if all_results:
        st.success(f"✅ Found {len(all_results)} jobs!")

        # Display each job
        for job in all_results:
            st.markdown(
                f"**{job['company']}** — *{job['keyword']}* — [{job['title']}]({job['link']})"
            )

        # Convert to DataFrame for CSV
        df = pd.DataFrame(all_results)
        csv = df.to_csv(index=False).encode('utf-8')

        # Download button
        st.download_button(
            label="⬇️ Download job list as CSV",
            data=csv,
            file_name='cyber_jobs.csv',
            mime='text/csv',
        )
    else:
        st.warning("❌ No jobs found.")
