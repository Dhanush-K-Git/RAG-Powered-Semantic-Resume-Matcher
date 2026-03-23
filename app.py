# --- STEP 1: SQLITE MONKEY PATCH (CRITICAL FOR DEPLOYMENT) ---
import sys
try:
    __import__('pysqlite3')
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
except ImportError:
    pass

# --- STEP 2: IMPORTS ---
import streamlit as st
import os
import pandas as pd
import shutil
from main import rank_resumes
from init_db import run_indexing

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="RAG-Powered Semantic Resume Matcher", 
    page_icon="🎯", 
    layout="wide"
)

# Custom CSS for the "Second Version" Look
st.html("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #1e1e1e;
        color: white;
        border: 1px solid #333;
    }
    .stButton>button:hover {
        border-color: #FF4B4B;
        color: #FF4B4B;
    }
    </style>
""")

# --- TITLE ---
st.title("RAG-Powered Semantic Resume Matcher 🎯")
st.markdown("---")

# --- INITIALIZE SESSION STATE ---
if "last_results" not in st.session_state:
    st.session_state.last_results = None

# --- SIDEBAR: SYSTEM CONTROLS ---
with st.sidebar:
    st.header("⚙️ Controls")
    if st.button("🚨 Hard Reset Vault"):
        if os.path.exists("./resume_vault"):
            shutil.rmtree("./resume_vault")
            st.warning("Vault wiped.")
        if os.path.exists("./data/resumes"):
            for f in os.listdir("./data/resumes"):
                os.remove(os.path.join("./data/resumes", f))

# --- MAIN INTERFACE: TWO COLUMN LAYOUT ---
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("1. Update Resume Vault")
    uploaded_files = st.file_uploader(
        "Upload PDF Resumes", 
        type=["pdf"], 
        accept_multiple_files=True
    )

    if st.button("📥 Add & Index Resumes"):
        if uploaded_files:
            with st.spinner("🔄 Indexing files..."):
                target_dir = os.path.join("data", "resumes")
                if not os.path.exists(target_dir):
                    os.makedirs(target_dir)
                
                for f in uploaded_files:
                    with open(os.path.join(target_dir, f.name), "wb") as buffer:
                        buffer.write(f.getbuffer())
                
                status = run_indexing()
                st.success(status)
        else:
            st.warning("Please upload PDF files.")

with col2:
    st.subheader("2. Job Match Requirements")
    jd_text = st.text_area(
        "Paste Job Description here:", 
        height=250, 
        placeholder="E.g., Looking for an AI Engineer with RAG experience..."
    )

st.divider()

# --- RANKING RESULTS ---
if st.button("🔍 Rank Best Candidates", use_container_width=True):
    if jd_text:
        with st.spinner("🧠 Calculating semantic match..."):
            results = rank_resumes(jd_text)
            
            if results:
                st.session_state.last_results = results
                st.subheader("🏆 Top Recommendations")
                
                table_data = []
                for i, r in enumerate(results):
                    score_pct = f"{round(r['Match Score'] * 100, 2)}%"
                    table_data.append({
                        "Rank": i + 1,
                        "Candidate Name": r["Candidate Name"],
                        "Match Score": score_pct
                    })
                
                st.dataframe(table_data, hide_index=True, use_container_width=True)
            else:
                st.error("No resumes found in the vault.")
    else:
        st.error("Please provide a Job Description.")

st.markdown("---")
st.caption("RAG-Powered Semantic Resume Matcher | Built by Dhanush Kumar | 2026")