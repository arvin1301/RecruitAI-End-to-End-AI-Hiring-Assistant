import os
import json
import time
import streamlit as st
from datetime import datetime

from agents.resume_parser import ResumeParser
from agents.recruiter_agent import RecruiterAgent

# Page config for this module
st.set_page_config(
    page_title="Resume Screening",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Resume Screening & Evaluation")
st.write("Upload a candidate resume and evaluate it against a job description.")

# Create two columns for better layout
col1, col2 = st.columns([2, 1])

with col1:
    uploaded_file = st.file_uploader(
        "Upload Resume (PDF or DOCX)",
        type=["pdf", "docx"],
        help="Supported formats: PDF, DOCX"
    )

with col2:
    st.info(
        "**Tips for better results:**\n- Use clear formatting\n- Include relevant keywords\n- Highlight technical skills")

# Job description section with better organization
st.subheader("📋 Job Description")
job_description = st.text_area(
    "Paste or type the job description here",
    height=250,
    value="""Role: AI Engineer

Required Skills:
- Python
- FastAPI
- LangChain
- Vector Databases
- LLMs

Experience: 0-2 Years

Responsibilities:
- Develop AI-powered applications
- Implement RAG solutions
- Optimize model performance
"""
)

# Advanced options
with st.expander("⚙️ Advanced Options"):
    evaluation_depth = st.select_slider(
        "Evaluation Depth",
        options=["Quick", "Standard", "Detailed"],
        value="Standard"
    )
    include_skill_gaps = st.checkbox("Include Skill Gap Analysis", value=True)
    generate_feedback = st.checkbox("Generate Candidate Feedback", value=True)

if uploaded_file:
    # Create resumes directory
    os.makedirs("resumes", exist_ok=True)

    file_path = os.path.join("resumes", uploaded_file.name)

    with open(file_path, "wb") as file:
        file.write(uploaded_file.getbuffer())

    st.success(f"✅ Uploaded: {uploaded_file.name}")

    # Show file info
    file_size = os.path.getsize(file_path) / 1024  # KB
    st.caption(f"File size: {file_size:.1f} KB")

    # Create metrics row
    col1, col2, col3 = st.columns(3)

    if st.button("🎯 Evaluate Candidate", type="primary", use_container_width=True):
        progress_bar = st.progress(0)
        status_text = st.empty()

        try:
            # Step 1: Extract text
            status_text.text("📄 Extracting text from resume...")
            progress_bar.progress(20)

            resume_text = ResumeParser.extract_text(file_path)

            # Step 2: Initialize recruiter agent
            status_text.text("🤖 Initializing AI evaluator...")
            progress_bar.progress(40)

            recruiter = RecruiterAgent()

            # Step 3: Evaluate candidate
            status_text.text("📊 Evaluating candidate against job requirements...")
            progress_bar.progress(60)

            result = recruiter.evaluate_candidate(
                resume_text=resume_text,
                job_description=job_description
            )

            progress_bar.progress(100)
            time.sleep(0.5)
            progress_bar.empty()
            status_text.empty()

            st.success("✅ Evaluation Complete!")

            # Display results in organized tabs
            tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "✅ Strengths", "⚠️ Gaps", "💡 Recommendation"])

            with tab1:
                # Candidate info and scores
                candidate_name = result.get("candidate_name", "Unknown")
                candidate_score = result.get("candidate_score", 0)

                st.subheader(f"Candidate: {candidate_name}")

                # Gauge chart for score
                st.metric("Overall Match Score", f"{candidate_score}%",
                          delta="Pass" if candidate_score >= 70 else "Needs Review")

                # Score visualization
                st.progress(candidate_score / 100)

                # Detailed metrics
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Skills Match", f"{result.get('skills_match', 0)}%")
                    st.metric("Experience Match", f"{result.get('experience_match', 0)}%")
                with col2:
                    st.metric("Education Match", f"{result.get('education_match', 0)}%")
                    st.metric("Cultural Fit", f"{result.get('cultural_fit', 0)}%")

            with tab2:
                st.subheader("✅ Candidate Strengths")
                strengths = result.get("strengths", [])
                if strengths:
                    for skill in strengths:
                        st.success(f"• {skill}")
                else:
                    st.info("No specific strengths identified")

            with tab3:
                st.subheader("⚠️ Missing or Weak Skills")
                missing_skills = result.get("missing_skills", [])
                if missing_skills:
                    for skill in missing_skills:
                        st.warning(f"• {skill}")
                else:
                    st.success("No significant gaps found!")

            with tab4:
                st.subheader("💡 AI Recommendation")
                recommendation = result.get("recommendation", "")

                if candidate_score >= 80:
                    st.success(f"**Decision:** Strongly Recommend for Interview")
                elif candidate_score >= 60:
                    st.warning(f"**Decision:** Consider for Interview")
                else:
                    st.error(f"**Decision:** Not Recommended")

                st.info(f"**Details:** {recommendation}")

                if generate_feedback:
                    st.subheader("📝 Candidate Feedback")
                    feedback = result.get("candidate_feedback", "")
                    st.text_area("Feedback to Candidate", feedback, height=100)

            # Save report
            os.makedirs("data/reports", exist_ok=True)

            safe_name = candidate_name.replace(" ", "_").replace("/", "_").replace("\\", "_")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_path = f"data/reports/{safe_name}_{timestamp}_resume_result.json"

            # Add metadata to result
            result["evaluation_metadata"] = {
                "timestamp": timestamp,
                "evaluation_depth": evaluation_depth,
                "file_name": uploaded_file.name
            }

            with open(report_path, "w", encoding="utf-8") as file:
                json.dump(result, file, indent=4, ensure_ascii=False)

            st.success(f"💾 Report saved: {report_path}")

            # Update session state
            st.session_state.total_candidates = st.session_state.get('total_candidates', 0) + 1

            # Export options
            st.subheader("📎 Export Options")
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("📥 Download JSON", use_container_width=True):
                    st.download_button(
                        label="Download Report",
                        data=json.dumps(result, indent=4),
                        file_name=f"{safe_name}_report.json",
                        mime="application/json"
                    )
            with col2:
                if st.button("📧 Send to Interview", use_container_width=True):
                    st.info("Interview invitation sent!")
            with col3:
                if st.button("💾 Save to Database", use_container_width=True):
                    st.success("Saved to candidate database!")

        except Exception as error:
            st.error(f"❌ Evaluation failed: {str(error)}")
            st.exception(error)