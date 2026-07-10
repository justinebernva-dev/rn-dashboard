import streamlit as st
import pandas as pd
import requests

# Set up page configurations with a custom title and business suitcase icon
st.set_page_config(
    page_title="RN Workspace Central",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CORPORATE BRANDING THEMING & COMPLETE STREAMLIT WHITE-LABELING ---
st.markdown("""
    <style>
    /* HIDE STREAMLIT LOGO, HEADER, FOOTER, AND MAIN MENU BUTTONS */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stDecoration"] {display: none;}
    
    /* Clean white background and professional gray text */
    .stApp {
        background-color: #ffffff;
        color: #2d3748;
        font-family: sans-serif;
    }
    
    /* Clean light gray sidebar */
    [data-testid="stSidebar"] {
        background-color: #f7fafc !important;
        border-right: 1px solid #e2e8f0;
    }
    
    /* Headers in crisp corporate dark gray */
    h1, h2, h3, h4 {
        color: #1a202c !important;
        font-weight: 700 !important;
    }
    
    /* Slate gray metric cards with a sharp top crimson highlight border */
    div[data-testid="stMetric"] {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-top: 4px solid #d60a0a; /* Premium Corporate Red accent */
        border-radius: 8px;
        padding: 15px !important;
        margin-bottom: 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    div[data-testid="stMetricValue"] {
        color: #d60a0a !important; /* Bold red for main numbers */
        font-weight: 700 !important;
    }
    div[data-testid="stMetricLabel"] {
        color: #4a5568 !important;
    }
    
    /* Clean custom styled app folders (expanders) */
    .stExpander {
        background-color: #fdfdfd !important;
        border: 1px solid #cbd5e0 !important;
        border-radius: 6px !important;
        margin-bottom: 10px !important;
    }
    
    /* Premium Crimson Red styling for the action buttons */
    .stDownloadButton button {
        background: #d60a0a !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        border-radius: 6px !important;
        border: none !important;
        padding: 8px 20px !important;
        box-shadow: 0 2px 4px rgba(214, 10, 10, 0.2);
        transition: background 0.2s ease !important;
    }
    .stDownloadButton button:hover {
        background: #b00808 !important; /* Slightly deeper red on tap/hover */
    }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR BRANDING ---
with st.sidebar:
    st.markdown("<h4 style='text-align: center; color: #1a202c;'>RN OPERATIONAL HUB</h4>", unsafe_allow_html=True)
    try:
        st.image("logo (1).jpg", use_container_width=True)
    except:
        st.info("💡 Add 'logo (1).jpg' to GitHub.")
    st.markdown("---")
    st.markdown("🔴 **System:** Core Active")

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
        row = {
            "Submission ID": sub.get("id"), 
            "Created At": sub.get("created_at"), 
            "Status": sub.get("status")
        }
        for key, value in answers.items():
            name = value.get("name")
            if name and "answer" in value:
                ans = value["answer"]
                row[name] = " ".join([str(v) for v in ans.values() if v]) if isinstance(ans, dict) else str(ans)
        parsed_data.append(row)
    return pd.DataFrame(parsed_data)

# --- MAIN INTERFACE ---
st.title("💼 RN Business Consulting — Workspace Central")
tab1, tab2 = st.tabs(["📊 Live Data Hub", "⚙️ System Configuration"])

with tab1:
    col1, col2 = st.columns(2, gap="large")
    
    # --- CLIENT AGREEMENTS ---
    with col1:
        st.subheader("📋 Client Agreements")
        raw_agreements = fetch_jotform_submissions(CLIENT_AGREEMENT_FORM_ID)
        
        if raw_agreements:
            df_agreements = parse_submissions(raw_agreements)
            st.metric("Total Portfolios", len(df_agreements))
            
            csv_agreements = df_agreements.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Export Master File", csv_agreements, "RN Dashboard - Client Agreements.csv", "text/csv")
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Drill-down by Client Name
            for _, row in df_agreements.iterrows():
                client_name = row.get('fullName_1', row.get('fullName', f"Client Record #{row['Submission ID']}"))
                
                with st.expander(f"👤 {client_name}"):
                    for col_name, value in row.items():
                        if col_name not in ['fullName_1', 'fullName'] and pd.notna(value):
                            st.markdown(f"**{col_name}:** {value}")
        else:
            st.info("No active records found.")

    # --- BENCHMARKING ---
    with col2:
        st.subheader("📈 Benchmarking Matrices")
        raw_benchmarks = fetch_jotform_submissions(BENCHMARKING_FORM_ID)
        
        if raw_benchmarks:
            df_benchmarks = parse_submissions(raw_benchmarks)
            st.metric("Profiles Analyzed", len(df_benchmarks))
            
            csv_benchmarks = df_benchmarks.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Export Master File", csv_benchmarks, "RN Dashboard - Benchmarking.csv", "text/csv")
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Drill-down by Business/Client Name
            for _, row in df_benchmarks.iterrows():
                bench_name = row.get('fullName_1', row.get('fullName', row.get('businessName', f"Benchmark #{row['Submission ID']}")))
                
                with st.expander(f"🏢 {bench_name}"):
                    for col_name, value in row.items():
                        if col_name not in ['fullName_1', 'fullName', 'businessName'] and pd.notna(value):
                            st.markdown(f"**{col_name}:** {value}")
        else:
            st.info("No active profiles found.")