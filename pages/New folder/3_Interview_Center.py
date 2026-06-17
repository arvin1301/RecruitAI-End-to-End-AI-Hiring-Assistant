import os
import json
import threading
import time
import streamlit as st
import plotly.graph_objects as go
from datetime import datetime

from agents.interview_agent import InterviewAgent
from agents.voice_agent import VoiceAgent
from agents.tts_agent import TTSAgent
from agents.proctoring_agent import ProctoringAgent

st.set_page_config(
    page_title="Interview Center",
    page_icon="🎤",
    layout="wide"
)

st.title("🎤 AI-Powered Interview Center")
st.write("Conduct comprehensive AI-driven interviews with proctoring")

# Initialize session state
if 'interview_started' not in st.session_state:
    st.session_state.interview_started = False
if 'current_question_index' not in st.session_state:
    st.session_state.current_question_index = 0

# Candidate information
st.header("👤 Candidate Information")
col1, col2 = st.columns(2)
with col1:
    candidate_name = st.text_input("Candidate Name", value="PH ARVIND SHARMA")
with col2:
    role = st.text_input("Position/Role", value="AI Engineer")

# Interview configuration
with st.expander("⚙️ Interview Configuration"):
    col1, col2 = st.columns(2)
    with col1:
        num_text_questions = st.number_input("Number of Text Questions", min_value=1, max_value=10, value=3)
        enable_proctoring = st.checkbox("Enable AI Proctoring", value=True)
    with col2:
        num_voice_questions = st.number_input("Number of Voice Questions", min_value=1, max_value=10, value=2)
        passing_score = st.slider("Passing Score Threshold", 0, 100, 70)

# Start interview button
if not st.session_state.interview_started:
    if st.button("🚀 Start Interview", type="primary", use_container_width=True):
        with st.spinner("Preparing interview questions..."):
            interview_agent = InterviewAgent()
            response = interview_agent.generate_questions(
                candidate_profile={
                    "candidate_name": candidate_name,
                    "strengths": ["Machine Learning", "Deep Learning", "NLP"]
                },
                role=role,
                num_questions=num_text_questions
            )
            st.session_state["questions"] = response["questions"]
            st.session_state.interview_started = True
            st.rerun()

# Interview flow
if st.session_state.interview_started:
    # Progress tracking
    progress = len(st.session_state.get("answers", [])) / max(1, len(st.session_state["questions"]))
    st.progress(progress)
    st.caption(f"Progress: {int(progress * 100)}% complete")

    # Text Interview Round
    st.header("📝 Text Interview Round")
    st.info("Please answer the following questions thoroughly.")

    answers = []

    for index, question in enumerate(st.session_state["questions"]):
        with st.container():
            st.markdown(f"### Question {index + 1}")
            st.write(question)

            # Store answer in session state
            answer_key = f"answer_{index}"
            default_answer = st.session_state.get(answer_key, "")
            answer = st.text_area(
                f"Your Answer",
                value=default_answer,
                key=answer_key,
                height=150,
                help="Provide a detailed answer"
            )
            answers.append(answer)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 Save Progress", use_container_width=True):
            st.session_state["answers"] = answers
            st.success("Progress saved!")

    with col2:
        if st.button("✅ Submit Text Round", type="primary", use_container_width=True):
            if any(not ans.strip() for ans in answers):
                st.warning("⚠️ Please answer all questions before submitting.")
            else:
                with st.spinner("Evaluating your answers..."):
                    interview_agent = InterviewAgent()
                    evaluations = []

                    progress_bar = st.progress(0)
                    for i, (question, answer) in enumerate(zip(st.session_state["questions"], answers)):
                        evaluation = interview_agent.evaluate_answer(question, answer)
                        evaluations.append(evaluation)
                        progress_bar.progress((i + 1) / len(answers))

                    text_report = interview_agent.generate_interview_report(evaluations)
                    st.session_state["text_report"] = text_report
                    st.rerun()

# Text Round Results
if "text_report" in st.session_state:
    text_report = st.session_state["text_report"]
    text_score = text_report.get("overall_score", 0)

    # Create gauge chart
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=text_score,
        title={"text": "Text Round Score"},
        domain={"x": [0, 1], "y": [0, 1]},
        gauge={
            "axis": {"range": [None, 100]},
            "bar": {"color": "darkblue"},
            "steps": [
                {"range": [0, 50], "color": "lightgray"},
                {"range": [50, 70], "color": "gray"},
                {"range": [70, 100], "color": "darkgreen"}
            ],
            "threshold": {
                "line": {"color": "red", "width": 4},
                "thickness": 0.75,
                "value": passing_score
            }
        }
    ))
    st.plotly_chart(fig, use_container_width=True)

    if text_score >= passing_score:
        st.success(f"✅ Text Round Cleared! Score: {text_score}%")

        # Voice Interview Section
        st.header("🎤 Voice Interview Round")
        st.info(
            "Camera monitoring will begin automatically. Please ensure good lighting and stable internet connection.")

        if st.button("🎙️ Start Proctored Voice Interview", type="primary", use_container_width=True):
            interview_agent = InterviewAgent()
            voice_agent = VoiceAgent()
            tts_agent = TTSAgent()
            proctoring_agent = ProctoringAgent()

            # Start monitoring
            if enable_proctoring:
                monitor_thread = threading.Thread(target=proctoring_agent.start_monitoring)
                monitor_thread.daemon = True
                monitor_thread.start()
                st.success("✅ AI Proctoring Started - Camera active")

            # Generate voice questions
            with st.spinner("Preparing voice interview questions..."):
                response = interview_agent.generate_questions(
                    candidate_profile={
                        "candidate_name": candidate_name,
                        "strengths": ["Machine Learning", "Deep Learning", "NLP"]
                    },
                    role=role,
                    num_questions=num_voice_questions
                )
                voice_questions = response["questions"]

            voice_evaluations = []
            st.info(f"🎤 You will be asked {len(voice_questions)} questions")

            # Voice interview loop
            for index, question in enumerate(voice_questions, start=1):
                st.markdown(f"### Voice Question {index}/{len(voice_questions)}")
                st.write(question)

                # Text-to-speech
                tts_agent.speak(question)

                # Recording
                st.info("🎙️ Recording in progress... Please speak clearly")
                time.sleep(2)  # Give user time to prepare

                transcript = voice_agent.record_and_transcribe()
                st.success(f"✅ Answer recorded: {len(transcript)} characters")

                # Evaluation
                with st.spinner("Evaluating response..."):
                    evaluation = interview_agent.evaluate_answer(question, transcript)
                    voice_evaluations.append(evaluation)

                    # Show instant feedback
                    st.metric("Technical Score", evaluation.get("technical_score", 0))
                    st.progress(evaluation.get("technical_score", 0) / 100)

            # Stop monitoring
            if enable_proctoring:
                proctoring_agent.stop_monitoring()
                risk_report = proctoring_agent.get_risk_score()
                st.session_state["risk_report"] = risk_report

            # Generate voice report
            voice_report = interview_agent.generate_interview_report(voice_evaluations)
            st.session_state["voice_report"] = voice_report

            # Update completed interviews count
            st.session_state.interviews_completed = st.session_state.get('interviews_completed', 0) + 1

            st.success("🎉 Interview Completed Successfully!")
            st.rerun()

    else:
        st.error(f"❌ Text Round Not Cleared. Score: {text_score}% (Required: {passing_score}%)")
        if st.button("🔄 Retry Text Round", use_container_width=True):
            del st.session_state["text_report"]
            st.rerun()

# Final Report Section
if all(key in st.session_state for key in ["text_report", "voice_report", "risk_report"]):
    st.header("🏆 Final Interview Report")

    text_report = st.session_state["text_report"]
    voice_report = st.session_state["voice_report"]
    risk_report = st.session_state["risk_report"]

    text_score = text_report.get("overall_score", 0)
    voice_score = voice_report.get("overall_score", 0)
    risk_score = risk_report.get("risk_score", 0)

    final_score = round(((text_score + voice_score) / 2) - (risk_score * 0.2), 2)
    recommendation = "Proceed" if final_score >= 70 else "Reject"

    # Display scores in columns
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Text Score", f"{text_score}%")
    with col2:
        st.metric("Voice Score", f"{voice_score}%")
    with col3:
        st.metric("Risk Score", f"{risk_score}%")
    with col4:
        st.metric("Final Score", f"{final_score}%")

    # Recommendation
    if recommendation == "Proceed":
        st.success("✅ Recommended for HR Review")
    else:
        st.error("❌ Not Recommended")

    # Save report
    os.makedirs("data/reports", exist_ok=True)

    report_data = {
        "candidate_name": candidate_name,
        "text_score": text_score,
        "voice_score": voice_score,
        "risk_score": risk_score,
        "final_score": final_score,
        "recommendation": recommendation,
        "text_report": text_report,
        "voice_report": voice_report,
        "risk_report": risk_report,
        "timestamp": datetime.now().isoformat()
    }

    with open("data/reports/interview_report.json", "w", encoding="utf-8") as file:
        json.dump(report_data, file, indent=4)

    st.success("💾 Interview report saved successfully!")