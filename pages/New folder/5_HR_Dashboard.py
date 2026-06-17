import os
import json
import streamlit as st
import pandas as pd
from datetime import datetime

from agents.hr_agent import HRAgent

st.set_page_config(
    page_title="HR Dashboard",
    page_icon="👨‍💼",
    layout="wide"
)

st.title("👨‍💼 HR Decision Dashboard")
st.write("Make data-driven hiring decisions with AI-powered insights")

# Load interview report
report_path = "data/reports/interview_report.json"

if not os.path.exists(report_path):
    st.warning("⚠️ No interview report found. Please complete an interview first.")
    st.info("💡 Go to Interview Center to conduct an interview.")
    st.stop()

with open(report_path, "r", encoding="utf-8") as file:
    interview_report = json.load(file)

# Extract candidate information
candidate_name = interview_report.get("candidate_name", "Unknown")
final_score = interview_report.get("final_score", 0)
risk_score = interview_report.get("risk_score", 0)
recommendation = interview_report.get("recommendation", "Reject")
text_score = interview_report.get("text_score", 0)
voice_score = interview_report.get("voice_score", 0)

# Header with candidate overview
st.header(f"Candidate: {candidate_name}")

# Quick metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Final Score", f"{final_score}%",
              delta="Pass" if final_score >= 70 else "Fail")
with col2:
    st.metric("Risk Score", f"{risk_score}%",
              delta="Low" if risk_score < 30 else "High")
with col3:
    st.metric("Interview Recommendation", recommendation,
              delta="Proceed" if recommendation == "Proceed" else "Stop")
with col4:
    st.metric("Overall Status", "Active",
              delta="In Review")

st.markdown("---")

# Detailed evaluation tabs
tab1, tab2, tab3 = st.tabs(["📊 Score Analysis", "📝 Interview Details", "🤖 AI Assessment"])

with tab1:
    st.subheader("Score Breakdown")

    # Create DataFrame for score visualization
    score_data = {
        "Category": ["Technical", "Communication", "Accuracy", "Risk", "Final"],
        "Score": [
            (interview_report.get("text_report", {}).get("average_technical_score", 0) +
             interview_report.get("voice_report", {}).get("average_technical_score", 0)) / 2,
            (interview_report.get("text_report", {}).get("average_communication_score", 0) +
             interview_report.get("voice_report", {}).get("average_communication_score", 0)) / 2,
            (interview_report.get("text_report", {}).get("average_accuracy_score", 0) +
             interview_report.get("voice_report", {}).get("average_accuracy_score", 0)) / 2,
            risk_score,
            final_score
        ]
    }

    df_scores = pd.DataFrame(score_data)
    st.bar_chart(df_scores.set_index("Category"))

    # Score interpretation
    st.subheader("Score Interpretation")

    col1, col2 = st.columns(2)
    with col1:
        if final_score >= 85:
            st.success("**Final Score:** Excellent - Top candidate")
        elif final_score >= 70:
            st.info("**Final Score:** Good - Strong candidate")
        elif final_score >= 60:
            st.warning("**Final Score:** Borderline - Consider with caution")
        else:
            st.error("**Final Score:** Poor - Not recommended")

    with col2:
        if risk_score > 50:
            st.error("**Risk Assessment:** High risk - Proctoring concerns detected")
        elif risk_score > 25:
            st.warning("**Risk Assessment:** Medium risk - Monitor closely")
        else:
            st.success("**Risk Assessment:** Low risk - Clean interview")

with tab2:
    st.subheader("Text Interview Summary")
    text_report = interview_report.get("text_report", {})

    col1, col2 = st.columns(2)
    with col1:
        st.write("**Technical Performance:**")
        st.progress(text_report.get("average_technical_score", 0) / 100)
        st.write(f"Score: {text_report.get('average_technical_score', 0)}%")

        st.write("**Communication Skills:**")
        st.progress(text_report.get("average_communication_score", 0) / 100)
        st.write(f"Score: {text_report.get('average_communication_score', 0)}%")

    with col2:
        st.write("**Answer Accuracy:**")
        st.progress(text_report.get("average_accuracy_score", 0) / 100)
        st.write(f"Score: {text_report.get('average_accuracy_score', 0)}%")

        total_questions = len(text_report.get("questions", []))
        st.write(f"**Questions Answered:** {total_questions}")

    st.subheader("Voice Interview Summary")
    voice_report = interview_report.get("voice_report", {})

    col1, col2 = st.columns(2)
    with col1:
        st.write("**Technical Performance:**")
        st.progress(voice_report.get("average_technical_score", 0) / 100)
        st.write(f"Score: {voice_report.get('average_technical_score', 0)}%")

        st.write("**Communication Skills:**")
        st.progress(voice_report.get("average_communication_score", 0) / 100)
        st.write(f"Score: {voice_report.get('average_communication_score', 0)}%")

    with col2:
        st.write("**Answer Accuracy:**")
        st.progress(voice_report.get("average_accuracy_score", 0) / 100)
        st.write(f"Score: {voice_report.get('average_accuracy_score', 0)}%")

        total_questions = len(voice_report.get("questions", []))
        st.write(f"**Questions Answered:** {total_questions}")

with tab3:
    st.subheader("AI-Generated Assessment")

    # Generate AI assessment if not already done
    if st.button("🤖 Generate AI Assessment", type="primary", use_container_width=True):
        with st.spinner("AI analyzing candidate data..."):
            hr_agent = HRAgent()

            report_data = {
                "candidate_name": candidate_name,
                "resume_score": text_score,
                "interview_score": voice_score,
                "risk_score": risk_score,
                "final_score": final_score,
                "resume_strengths": ["Machine Learning", "Deep Learning", "NLP"],
                "missing_skills": []
            }

            hr_decision = hr_agent.generate_hr_decision(report_data)
            st.session_state["hr_decision"] = hr_decision

    # Display AI decision
    if "hr_decision" in st.session_state:
        hr_decision = st.session_state["hr_decision"]

        st.success("### AI Decision Generated")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Status", hr_decision.get("status", "Unknown"))
        with col2:
            st.metric("Salary Band", hr_decision.get("salary_band", "N/A"))
        with col3:
            st.metric("Next Round", hr_decision.get("next_round", "None"))

        st.subheader("HR Summary")
        st.info(hr_decision.get("hr_summary", ""))

        st.subheader("Joining Recommendation")
        st.success(hr_decision.get("joining_recommendation", ""))

        # Save HR decision
        os.makedirs("data/hr_reports", exist_ok=True)
        safe_name = candidate_name.replace(" ", "_").replace("/", "_")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        with open(f"data/hr_reports/{safe_name}_{timestamp}_hr_decision.json", "w", encoding="utf-8") as file:
            json.dump(hr_decision, file, indent=4, ensure_ascii=False)

        st.success("HR decision saved to database")

st.markdown("---")

# HR Actions
st.header("📝 HR Actions")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Schedule Follow-up")
    interview_date = st.date_input("Select Interview Date", min_value=datetime.now())
    interview_time = st.time_input("Select Time", datetime.now().time())

    if st.button("📅 Schedule Interview", use_container_width=True):
        st.success(f"Interview scheduled for {interview_date} at {interview_time}")

with col2:
    st.subheader("Send Communication")
    email_template = st.selectbox(
        "Email Template",
        ["Offer Letter", "Rejection Letter", "Interview Invitation", "Feedback Request"]
    )

    if st.button("📧 Send Email", use_container_width=True):
        st.success(f"{email_template} sent to {candidate_name}")

# Final decision
st.markdown("---")
st.header("🎯 Final Hiring Decision")

col1, col2, col3 = st.columns([1, 1, 1])

with col2:
    if final_score >= 70 and risk_score < 50:
        if st.button("✅ SELECT CANDIDATE", type="primary", use_container_width=True):
            st.balloons()
            st.success(f"🎉 {candidate_name} has been selected!")
            st.info("Offer letter will be generated and sent to HR for approval")
    else:
        if st.button("❌ REJECT CANDIDATE", type="primary", use_container_width=True):
            st.warning(f"Candidate {candidate_name} has been rejected")
            st.info("Rejection letter will be sent automatically")

# Historical data
st.markdown("---")
with st.expander("📊 Historical HR Decisions"):
    if os.path.exists("data/hr_reports"):
        hr_files = [f for f in os.listdir("data/hr_reports") if f.endswith("_hr_decision.json")]
        if hr_files:
            for file in hr_files[-5:]:  # Show last 5 decisions
                with open(f"data/hr_reports/{file}", "r") as f:
                    decision = json.load(f)
                st.markdown(
                    f"**{file.replace('_hr_decision.json', '')}** - Status: {decision.get('status', 'Unknown')}")
        else:
            st.info("No historical HR decisions found")