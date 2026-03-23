import streamlit as st
import os
import pandas as pd
from main import rank_resumes
from init_db import run_indexing

# --- PAGE CONFIG ---
st.set_page_config(page_title="RAG-Powered Semantic Resume Matcher", page_icon="🎯", layout="wide")
st.title("RAG-Powered Semantic Resume Matcher 🎯")
st.markdown("---")

# --- INITIALIZE SESSION STATE ---
if "last_results" not in st.session_state:
    st.session_state.last_results = None

# --- SIDEBAR: SYSTEM CONTROLS ---
with st.sidebar:
    st.header("⚙️ Controls")
    st.info("This tool uses Local Vector Search (S-BERT) to rank candidates by semantic match.")
    
    if st.button("🚨 Hard Reset Vault", use_container_width=True):
        if os.path.exists("./resume_vault"):
            import shutil
            shutil.rmtree("./resume_vault")
            st.warning("Vault wiped. Please re-index resumes.")

# --- MAIN INTERFACE: UPLOAD & RANK ---
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("1. Update Resume Vault")
    uploaded_files = st.file_uploader(
        "Upload PDF Resumes", 
        type=["pdf"], 
        accept_multiple_files=True
    )

    if st.button("📥 Add & Index Resumes", use_container_width=True):
        if uploaded_files:
            with st.spinner("🔄 Wiping old memory and indexing new files..."):
                target_dir = os.path.join("data", "resumes")
                if not os.path.exists(target_dir):
                    os.makedirs(target_dir)
                
                # Cleanup old files
                for old_file in os.listdir(target_dir):
                    os.unlink(os.path.join(target_dir, old_file))

                # Save new files
                for f in uploaded_files:
                    with open(os.path.join(target_dir, f.name), "wb") as buffer:
                        buffer.write(f.getbuffer())
                
                # Run local indexing
                status = run_indexing()
                st.success(status)
        else:
            st.warning("Please upload at least one PDF.")

with col2:
    st.subheader("2. Job Match Requirements")
    jd_text = st.text_area(
        "Paste Job Description here:", 
        height=200, 
        placeholder="E.g., We are looking for an AI Engineer with experience in RAG and LangGraph..."
    )

st.divider()

# --- RANKING RESULTS SECTION ---
if st.button("🔍 Rank Best Candidates", use_container_width=True):
    if jd_text:
        with st.spinner("🧠 Calculating semantic match scores..."):
            results = rank_resumes(jd_text)
            
            if results:
                st.session_state.last_results = results
                st.subheader("🏆 Top Recommendations")
                
                # Create a clean table list
                table_list = []
                for i, r in enumerate(results):
                    table_list.append({
                        "Rank": i + 1,
                        "Candidate Name": r["Candidate Name"],
                        "Match Score": r["Match Score"]
                    })
                
                # Display the data in a sleek, non-indexed table
                st.dataframe(table_list, hide_index=True, use_container_width=True)
            else:
                st.error("No resumes found. Please index files first.")
    else:
        st.error("Please provide a Job Description to start.")

st.markdown("---")
st.caption("AI Resume Matcher | Built by Dhanush Kumar | Powered by ChromaDB & Sentence Transformers")