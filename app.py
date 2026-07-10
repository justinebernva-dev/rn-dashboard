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
    .stApp { background-color: #0e1117; color: #e0e6ed; font-family: sans-serif; }
    h1 { color: #00f2fe; font-weight: 800 !important; }
    h2, h3 { color: #4facfe !important; }
    div[data-testid="stMetric"] {
        background: linear-gradient(145deg, #1f242e, #161a23);
        border: 1px solid #2b3344;
        border-radius: 12px;
        padding: 15px !important;
    }
    div[data-testid="stMetricValue"] { color: #00f2fe !important; }
    .stDownloadButton button {
        background: linear-gradient(45deg, #4facfe 0%, #00f2fe 100%) !important;
        color: #0e1117 !important;
        font-weight: 700 !important;
        border-radius: 8px !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR BRANDING ---
with st.sidebar:
    st.markdown("<h3 style='text-align: center; color: #00f2fe;'>OPERATIONS CORE</h3>", unsafe_allow_html=True)
    try:
        st.image("logo (1).jpg", use_container_width=True)
    except:
        st.info("💡 Add 'logo (1).jpg' to GitHub.")
    st.markdown("---")
    st.markdown("🟢 **System Status:** Operational")

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
    except:
        return []

def parse_submissions(submissions):
    parsed_data = []
    for sub in submissions:
        answers = sub.get("answers", {})
        row = {"Submission ID": sub.get("id"), "Created At": sub.get("created_at"), "Status": sub.get("status")}
        for key, value in answers.items():
            name = value.get("name")
            if name and "answer" in value:
                ans = value["answer"]
                row[name] = " ".join([str(v) for v in ans.values() if v]) if isinstance(ans, dict) else str(ans)
        parsed_data.append(row)
    return pd.DataFrame(parsed_data)

# --- MAIN INTERFACE ---
st.title("⚡ RN Business Consulting — Workspace Central")
tab1, tab2 = st.tabs(["📊 Live Data Hub", "🛡️ Security Diagnostics"])

with tab1:
    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.subheader("📋 Client Agreements")
        raw_agreements = fetch_jotform_submissions(CLIENT_AGREEMENT_FORM_ID)
        if raw_agreements:
            df = parse_submissions(raw_agreements)
            st.metric("Total", len(df))
            st.dataframe(df, use_container_width=True)
            st.download_button("📥 Export CSV", df.to_csv(index=False).encode('utf-8'), "agreements.csv", "text/csv")
        else:
            st.info("No data.")
    with col2:
        st.subheader("📈 Benchmarking Matrices")
        raw_benchmarks = fetch_jotform_submissions(BENCHMARKING_FORM_ID)
        if raw_benchmarks:
            df = parse_submissions(raw_benchmarks)
            st.metric("Total", len(df))
            st.dataframe(df, use_container_width=True)
            st.download_button("📥 Export CSV", df.to_csv(index=False).encode('utf-8'), "benchmarks.csv", "text/csv")
        else:
            st.info("No data.")