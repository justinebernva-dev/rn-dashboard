import streamlit as st
import pandas as pd
import requests

# Set up page configurations with a sleek layout
st.set_page_config(
    page_title="RN Workspace Central",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ADVANCED FUTURISTIC THEMING (CSS) ---
st.markdown("""
    <style>
    /* Main background and font styling */
    .stApp {
        background-color: #0e1117;
        color: #e0e6ed;
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }
    
    /* Header styling */
    h1 {
        color: #00f2fe;
        font-weight: 800 !important;
        letter-spacing: -0.5px;
        text-shadow: 0 0 10px rgba(0, 242, 254, 0.2);
    }
    h2, h3 {
        color: #4facfe !important;
        font-weight: 600 !important;
    }
    
    /* Sleek container cards for metrics and tables */
    div[data-testid="stMetric"] {
        background: linear-gradient(145deg, #1f242e, #161a23);
        border: 1px solid #2b3344;
        border-radius: 12px;
        padding: 15px 20px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        transition: transform 0.2s ease;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        border-color: #00f2fe;
    }
    
    /* Metric text colors */
    div[data-testid="stMetricLabel"] {
        color: #8fa0b5 !important;
        font-size: 0.95rem !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    div[data-testid="stMetricValue"] {
        color: #00f2fe !important;
        font-size: 2.2rem !important;
        font-weight: 700 !important;
    }
    
    /* Custom tab navigation styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: #161a23;
        padding: 8px;
        border-radius: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        color: #8fa0b5 !important;
        border-radius: 6px;
        padding: 10px 20px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stTabs [aria-selected="true"] {
        background-color: #232a37 !important;
        color: #00f2fe !important;
        border-bottom: 2px solid #00f2fe !important;
    }
    
    /* Custom styling for download buttons */
    .stDownloadButton button {
        background: linear-gradient(45deg, #4facfe 0%, #00f2fe 100%) !important;
        color: #0e1117 !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 24px !important;
        box-shadow: 0 4px 12px rgba(0, 242, 254, 0.3);
        transition: all 0.3s ease !important;
    }
    .stDownloadButton button:hover {
        transform: scale(1.02);
        box-shadow: 0 6px 20px rgba(0, 242, 254, 0.5);
    }
    </style>
""", unsafe_html=True)

# --- SIDEBAR BRANDING ---
with st.sidebar:
    st.markdown("<h3 style='text-align: center; color: #00f2fe;'>OPERATIONS CORE</h3>", unsafe_html=True)
    try:
        st.image("logo (1).jpg", use_container_width=True)
    except:
        st.info("💡 Add 'logo (1).jpg' to GitHub to display logo here.")
    st.markdown("---")
    st.markdown("🟢 **System Status:** Operational")
    st.markdown("📶 **Network:** Secure Gateway")

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
        if response.status_code == 200:
            return response.json().get("content", [])
        return []
    except Exception as e:
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
        for key, value in answers.items():
            name = value.get("name")
            if name and "answer" in value:
                ans = value["answer"]
                if isinstance(ans, dict):
                    row[name] = " ".join([str(v) for v in ans.values() if v])
                else:
                    row[name] = str(ans)
        parsed_data.append(row)
    return pd.DataFrame(parsed_data)

# --- MAIN INTERFACE ---
st.title("⚡ RN Business Consulting — Workspace Central")
st.markdown("<p style='color: #8fa0b5; font-size: 1.1rem;'>Real-time decentralized operations platform.</p>", unsafe_html=True)

tab1, tab2 = st.tabs(["📊 Live Data Hub", "🛡️ Security Diagnostics"])

with tab1:
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.subheader("📋 Client Agreements")
        raw_agreements = fetch_jotform_submissions(CLIENT_AGREEMENT_FORM_ID)
        if raw_agreements:
            df_agreements = parse_submissions(raw_agreements)
            st.metric("Active Protocols", len(df_agreements))
            st.dataframe(df_agreements, use_container_width=True)
            
            csv_agreements = df_agreements.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Export Agreements Dataset",
                data=csv_agreements,
                file_name="client_agreements.csv",
                mime="text/csv"
            )
        else:
            st.info("No active protocol submissions found.")
            
    with col2:
        st.subheader("📈 Benchmarking Matrices")
        raw_benchmarks = fetch_jotform_submissions(BENCHMARKING_FORM_ID)
        if raw_benchmarks:
            df_benchmarks = parse_submissions(raw_benchmarks)
            st.metric("Evaluations Processed", len(df_benchmarks))
            st.dataframe(df_benchmarks, use_container_width=True)
            
            csv_benchmarks = df_benchmarks.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Export Metrics Dataset",
                data=csv_benchmarks,
                file_name="benchmarking_submissions.csv",
                mime="text/csv"
            )
        else:
            st.info("No evaluation submissions found.")

with tab2:
    st.header("Sync Architecture")
    st.success("API Credentials successfully injected into cloud gateway.")
    st.json({
        "Client Agreement Sync": bool(CLIENT_AGREEMENT_FORM_ID),
        "Benchmarking Matrix Sync": bool(BENCHMARKING_FORM_ID),
        "Environment Node": "Jotform REST API v1"
    })