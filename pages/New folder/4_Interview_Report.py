import os
import json
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime

st.set_page_config(
    page_title="Interview Report",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Comprehensive Interview Report Dashboard")
st.write("Detailed analytics and insights from AI-powered interviews")

# Load report
report_path = "data/reports/interview_report.json"

if not os.path.exists(report_path):
    st.warning("⚠️ No interview report found. Please complete an interview first.")
    st.info("💡 Go to Interview Center to conduct an interview.")
    st.stop()

with open(report_path, "r", encoding="utf-8") as file:
    report = json.load(file)

# Extract data
candidate_name = report.get("candidate_name", "Unknown")
text_score = report.get("text_score", 0)
voice_score = report.get("voice_score", 0)
risk_score = report.get("risk_score", 0)
final_score = report.get("final_score", 0)
recommendation = report.get("recommendation", "N/A")
timestamp = report.get("timestamp", datetime.now().isoformat())

# Header with candidate info
col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    st.header(f"👤 Candidate: {candidate_name}")
with col2:
    st.metric("Interview Date", datetime.fromisoformat(timestamp).strftime("%Y-%m-%d"))
with col3:
    st.metric("Report ID", hash(timestamp) % 10000)

st.markdown("---")

# Score Overview with gauges
st.subheader("📊 Performance Overview")

# Create gauge charts
col1, col2, col3, col4 = st.columns(4)

with col1:
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=text_score,
        title={"text": "Text Score"},
        domain={"x": [0, 1], "y": [0, 1]},
        gauge={"axis": {"range": [0, 100]}, "bar": {"color": "darkblue"}}
    ))
    fig.update_layout(height=250)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=voice_score,
        title={"text": "Voice Score"},
        domain={"x": [0, 1], "y": [0, 1]},
        gauge={"axis": {"range": [0, 100]}, "bar": {"color": "green"}}
    ))
    fig.update_layout(height=250)
    st.plotly_chart(fig, use_container_width=True)

with col3:
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=risk_score,
        title={"text": "Risk Score"},
        domain={"x": [0, 1], "y": [0, 1]},
        gauge={"axis": {"range": [0, 100]},
               "bar": {"color": "red"},
               "threshold": {"value": 30, "line": {"color": "orange", "width": 4}}}
    ))
    fig.update_layout(height=250)
    st.plotly_chart(fig, use_container_width=True)

with col4:
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=final_score,
        title={"text": "Final Score"},
        domain={"x": [0, 1], "y": [0, 1]},
        gauge={"axis": {"range": [0, 100]},
               "bar": {"color": "purple"},
               "steps": [
                   {"range": [0, 60], "color": "lightgray"},
                   {"range": [60, 80], "color": "gray"},
                   {"range": [80, 100], "color": "darkgreen"}
               ]}
    ))
    fig.update_layout(height=250)
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Recommendation
if recommendation == "Proceed":
    st.success("✅ **RECOMMENDATION:** Proceed to HR Review")
else:
    st.error("❌ **RECOMMENDATION:** Not Recommended for Next Round")

st.markdown("---")

# Detailed Evaluations
st.header("📋 Detailed Question Analysis")

text_report = report.get("text_report", {})
voice_report = report.get("voice_report", {})

# Create two columns for text and voice analysis
col1, col2 = st.columns(2)

with col1:
    st.subheader("📝 Text Interview Analysis")

    text_questions = text_report.get("questions", [])
    if text_questions:
        for i, q in enumerate(text_questions, 1):
            with st.expander(f"Question {i}"):
                st.write(f"**Question:** {q.get('question', 'N/A')}")
                st.write(f"**Technical Score:** {q.get('technical_score', 0)}/100")
                st.write(f"**Communication:** {q.get('communication_score', 0)}/100")
                st.write(f"**Accuracy:** {q.get('accuracy_score', 0)}/100")
                st.progress(q.get('technical_score', 0) / 100)

    st.metric("Average Technical Score", f"{text_report.get('average_technical_score', 0)}%")
    st.metric("Average Communication Score", f"{text_report.get('average_communication_score', 0)}%")
    st.metric("Average Accuracy Score", f"{text_report.get('average_accuracy_score', 0)}%")

with col2:
    st.subheader("🎤 Voice Interview Analysis")

    voice_questions = voice_report.get("questions", [])
    if voice_questions:
        for i, q in enumerate(voice_questions, 1):
            with st.expander(f"Question {i}"):
                st.write(f"**Question:** {q.get('question', 'N/A')}")
                st.write(f"**Technical Score:** {q.get('technical_score', 0)}/100")
                st.write(f"**Communication:** {q.get('communication_score', 0)}/100")
                st.write(f"**Accuracy:** {q.get('accuracy_score', 0)}/100")
                st.progress(q.get('technical_score', 0) / 100)

    st.metric("Average Technical Score", f"{voice_report.get('average_technical_score', 0)}%")
    st.metric("Average Communication Score", f"{voice_report.get('average_communication_score', 0)}%")
    st.metric("Average Accuracy Score", f"{voice_report.get('average_accuracy_score', 0)}%")

st.markdown("---")

# Proctoring Report
st.header("📷 AI Proctoring Analysis")

risk_report = report.get("risk_report", {})

# Proctoring metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Phone Usage Events", risk_report.get("phone_events", 0),
              delta="Suspicious" if risk_report.get("phone_events", 0) > 0 else "Clean")
with col2:
    st.metric("Multiple Persons Detected", risk_report.get("multiple_person_events", 0),
              delta="Alert" if risk_report.get("multiple_person_events", 0) > 0 else "Clean")
with col3:
    st.metric("Face Missing Events", risk_report.get("missing_person_events", 0),
              delta="Warning" if risk_report.get("missing_person_events", 0) > 0 else "Good")
with col4:
    st.metric("Overall Risk Level",
              "High" if risk_score > 50 else ("Medium" if risk_score > 25 else "Low"),
              delta=f"Score: {risk_score}")

# Proctoring timeline (placeholder for actual data)
st.subheader("Proctoring Timeline")
st.info("📊 Proctoring timeline visualization would appear here with timestamps of events")

st.markdown("---")

# Hiring Decision Summary
st.header("🧠 Hiring Readiness Assessment")

# Score interpretation
score_ranges = {
    "Excellent Candidate": (85, 100),
    "Good Candidate": (70, 85),
    "Borderline Candidate": (60, 70),
    "Weak Candidate": (0, 60)
}

for level, (min_score, max_score) in score_ranges.items():
    if min_score <= final_score <= max_score:
        if final_score >= 85:
            st.success(f"### {level} 🏆")
            st.write("Strongly recommended for immediate hiring")
        elif final_score >= 70:
            st.info(f"### {level} 👍")
            st.write("Recommended for further consideration")
        elif final_score >= 60:
            st.warning(f"### {level} ⚠️")
            st.write("Consider with caution, may need additional assessment")
        else:
            st.error(f"### {level} ❌")
            st.write("Not recommended for current position")

# Strengths and Weaknesses Summary
st.markdown("---")
st.header("📈 Summary Insights")

col1, col2 = st.columns(2)

with col1:
    st.subheader("✅ Key Strengths")
    strengths = [
        "Strong technical knowledge" if text_report.get('average_technical_score', 0) > 70 else None,
        "Good communication skills" if voice_report.get('average_communication_score', 0) > 70 else None,
        "High accuracy in responses" if text_report.get('average_accuracy_score', 0) > 70 else None,
        "Clear verbal articulation" if voice_report.get('average_technical_score', 0) > 70 else None
    ]
    strengths = [s for s in strengths if s]
    if strengths:
        for strength in strengths:
            st.success(f"• {strength}")
    else:
        st.info("No significant strengths identified")

with col2:
    st.subheader("⚠️ Areas for Improvement")
    weaknesses = [
        "Technical knowledge needs improvement" if text_report.get('average_technical_score', 0) < 60 else None,
        "Communication clarity needs work" if voice_report.get('average_communication_score', 0) < 60 else None,
        "Answer accuracy could be better" if text_report.get('average_accuracy_score', 0) < 60 else None,
        "Proctoring concerns detected" if risk_score > 30 else None
    ]
    weaknesses = [w for w in weaknesses if w]
    if weaknesses:
        for weakness in weaknesses:
            st.warning(f"• {weakness}")
    else:
        st.success("No major areas for improvement identified")

st.markdown("---")

# Export and Share Options
st.header("📎 Report Actions")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("📥 Download PDF Report", use_container_width=True):
        st.info("PDF generation would be implemented here")

with col2:
    if st.button("📧 Email to HR", use_container_width=True):
        st.success("Report sent to HR department!")

with col3:
    if st.button("💾 Save to Database", use_container_width=True):
        st.success("Report saved to central database")

with col4:
    if st.button("🔄 Generate New Report", use_container_width=True):
        st.info("Navigate to Interview Center for new interview")

st.caption(f"Report generated on {datetime.fromisoformat(timestamp).strftime('%Y-%m-%d %H:%M:%S')}")