import streamlit as st
import os
import logging
from dotenv import load_dotenv
from src.parser import extract_text_from_pdf
from src.agent_graph import build_optimatch_graph

# Mute the background Google GenAI AFC warnings
logging.getLogger("google").setLevel(logging.ERROR)

load_dotenv()

# ... (keep the rest of your app.py the same) ...

st.set_page_config(page_title="OptiMatch AI", layout="wide")
st.title("🚀 OptiMatch AI: Employability & ATS Optimization Platform")

if not os.getenv("GOOGLE_API_KEY"):
    st.error("Missing GOOGLE_API_KEY in the .env file.")

col1, col2 = st.columns([1, 1.5])

with col1:
    st.subheader("1. Candidate Data")
    uploaded_file = st.file_uploader("Upload Resume (PDF)", type="pdf")
    job_description = st.text_area("Paste Target Job Description", height=250)
    analyze_btn = st.button("Run OptiMatch Analysis", type="primary")

with col2:
    st.subheader("2. AI Analysis Engine")
    if analyze_btn and uploaded_file and job_description:
        with st.spinner("Extracting text from document..."):
            resume_text = extract_text_from_pdf(uploaded_file)
            
        with st.spinner("Running Multi-Agent Workflow (Profiler -> Benchmarker -> Optimizer)..."):
            graph = build_optimatch_graph()
            initial_state = {
                "resume_text": resume_text,
                "job_description": job_description,
                "extracted_profile": "",
                "gap_analysis": "",
                "recommendations": ""
            }
            
            # --- THE NEW TRY/EXCEPT BLOCK STARTS HERE ---
            try:
                result = graph.invoke(initial_state)
                
                st.success("Workflow Complete!")
                
                with st.expander("1. Candidate Profile (Extracted)", expanded=False):
                    st.write(result["extracted_profile"])
                    
                with st.expander("2. Skill Gap Analysis (JD Benchmark)", expanded=True):
                    st.write(result["gap_analysis"])
                    
                with st.expander("3. Actionable Recommendations (ATS Optimization)", expanded=True):
                    st.write(result["recommendations"])
                    
            except Exception as e:
                st.error("⚠️ Google's AI API is currently experiencing high traffic. Please wait a few seconds and click Analyze again.")
            # --- END OF NEW BLOCK ---
                
    elif analyze_btn:
        st.warning("Please provide both a resume PDF and a job description.")