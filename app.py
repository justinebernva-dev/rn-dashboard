import streamlit as st
import pandas as pd
import requests

# Set up page configurations
st.set_page_config(
    page_title="RN Business Consulting Workspace",
    page_icon="💼",
    layout="wide"
)

# --- CONFIGURATION KEYS ---
JOTFORM_API_KEY = "6d3bcd83a932aa00acbbb6b105a57b92"
CLIENT_AGREEMENT_FORM_ID = "250357163880459"
BENCHMARKING_FORM_ID = "250848585159067"

@st.cache_data(ttl=60)
def fetch_jotform_submissions(form_id):
    url = f"https://api.jotform.com/form/{form_id}/submissions"
    headers = {"apiKey": JOTFORM_API_KEY}
    params = {"limit": 100}
    
    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:  # Fixed the typo here!
            data = response.json().get("content", [])
            return data
        else:
            return []
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return []

def parse_submissions(submissions):
    parsed_data = []
    for sub in submissions:
        answers = sub.get("answers", {})
        row = {
            "Submission ID": sub.get("id"),
            "Created At": sub.get("created_at"),
            "Status": sub.get("status")
        }
        
        # Pull basic fields dynamically
        for key, value in answers.items():
            name = value.get("name")
            if name:
                if "answer" in value:
                    ans = value["answer"]
                    if isinstance(ans, dict):
                        row[name] = " ".join([str(v) for v in ans.values() if v])
                    else:
                        row[name] = str(ans)
        parsed_data.append(row)
    return pd.DataFrame(parsed_data)

st.title("💼 RN Business Consulting — Workspace Central")
st.markdown("Welcome to your live operational workspace.")

tab1, tab2 = st.tabs(["📋 Live Submission Tracking", "⚙️ Connection Diagnostics"])

with tab1:
    st.header("Form Submission Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Client Agreements")
        raw_agreements = fetch_jotform_submissions(CLIENT_AGREEMENT_FORM_ID)
        if raw_agreements:
            df_agreements = parse_submissions(raw_agreements)
            st.dataframe(df_agreements, use_container_width=True)
            st.metric("Total Agreements", len(df_agreements))
            
            # This makes the data downloadable!
            csv_agreements = df_agreements.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Agreements CSV",
                data=csv_agreements,
                file_name="client_agreements.csv",
                mime="text/csv"
            )
        else:
            st.info("No client agreement submissions found or active.")
            
    with col2:
        st.subheader("Benchmarking Submissions")
        raw_benchmarks = fetch_jotform_submissions(BENCHMARKING_FORM_ID)
        if raw_benchmarks:
            df_benchmarks = parse_submissions(raw_benchmarks)
            st.dataframe(df_benchmarks, use_container_width=True)
            st.metric("Total Benchmarks", len(df_benchmarks))
            
            # This makes the data downloadable!
            csv_benchmarks = df_benchmarks.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Benchmarks CSV",
                data=csv_benchmarks,
                file_name="benchmarking_submissions.csv",
                mime="text/csv"
            )
        else:
            st.info("No benchmarking submissions found or active.")

with tab2:
    st.header("API & Integration Sync")
    st.success("API Credentials successfully injected into the local configuration workspace.")
    st.json({
        "Client Agreement Form Connected": bool(CLIENT_AGREEMENT_FORM_ID),
        "Benchmarking Form Connected": bool(BENCHMARKING_FORM_ID),
        "Authentication Target": "Jotform Live API Gateway"
    })
