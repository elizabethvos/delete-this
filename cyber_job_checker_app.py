import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("SERPAPI_KEY")

companies = [
    "Accenture", "Crowdstrike", "Cisco", "Microsoft", "Leidos", "Surface Cyber", "Booz Allen Hamilton"
]

keywords = ["cybersecurity", "security analyst", "GRC", "vulnerability", "infosec"]

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

st.title("🔍 Cybersecurity Job Checker")

if st.button("Check for Cyber Jobs"):
    all_results = []
    for company in companies:
        all_results.extend(search_jobs(company))
    if all_results:
        for job in all_results:
            st.markdown(f"**{job['company']}** — *{job['keyword']}* — [{job['title']}]({job['link']})")
    else:
        st.warning("No jobs found.")
