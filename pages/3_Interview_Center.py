import os
import json
import threading

import streamlit as st

from agents.interview_agent import InterviewAgent
from agents.voice_agent import VoiceAgent
from agents.tts_agent import TTSAgent
from agents.proctoring_agent import ProctoringAgent

st.set_page_config(
    page_title="Interview Center · RecruitAI",
    page_icon="",
    layout="wide"
)

# ─────────────────────────────────────────────
# Page header
# ─────────────────────────────────────────────
st.markdown(
    "<h2 style='margin-bottom:0.25rem;'> Interview Center</h2>"
    "<p style='color:#666; margin-bottom:1.5rem;'>"
    "Run a two-round interview (text → voice) with live AI proctoring.</p>",
    unsafe_allow_html=True
)

# ─────────────────────────────────────────────
# Pre-fill from Resume Screening if available
# ─────────────────────────────────────────────
default_name = st.session_state.get(
    "interview_candidate_name", ""
)
default_strengths = st.session_state.get(
    "interview_strengths",
    ["Machine Learning", "Deep Learning", "NLP"]
)

# ─────────────────────────────────────────────
# Candidate setup
# ─────────────────────────────────────────────
with st.container(border=True):
    setup_col1, setup_col2 = st.columns(2)
    with setup_col1:
        candidate_name = st.text_input(
            "Candidate name",
            value=default_name,
            placeholder="e.g. Arvind Sharma"
        )
    with setup_col2:
        role = st.text_input(
            "Role",
            value="AI Engineer",
            placeholder="e.g. AI Engineer"
        )

if not candidate_name.strip():
    st.info("Enter the candidate's name above to begin.")
    st.stop()

# ─────────────────────────────────────────────
# Pipeline progress indicator
# ─────────────────────────────────────────────
def _progress_html(text_done: bool, voice_done: bool) -> str:
    stages = [
        ("text",  " Text round",   text_done,           False),
        ("voice", " Voice round",  voice_done,          text_done and not voice_done),
        ("hr",    " HR review",    text_done and voice_done, False),
    ]
    items = []
    for _, label, done, active in stages:
        if done:
            color, bg = "#27500A", "#EAF3DE"
            icon = "✓"
        elif active:
            color, bg = "#3C3489", "#EEEDFE"
            icon = "●"
        else:
            color, bg = "#AAAAAA", "#F5F5F5"
            icon = "○"
        items.append(
            f"<div style='display:flex; align-items:center; gap:6px;'>"
            f"  <span style='width:22px; height:22px; border-radius:50%;"
            f"               background:{bg}; color:{color};"
            f"               font-size:12px; font-weight:600;"
            f"               display:inline-flex; align-items:center;"
            f"               justify-content:center;'>{icon}</span>"
            f"  <span style='font-size:13px; color:{color}; font-weight:500;'>"
            f"    {label}</span>"
            f"</div>"
        )
    return (
        "<div style='display:flex; gap:24px; flex-wrap:wrap;"
        "           margin-bottom:1.25rem; padding:12px 16px;"
        "           background:#FAFAFA; border-radius:10px;"
        "           border:1px solid #EBEBEB;'>"
        + "".join(items)
        + "</div>"
    )

text_done  = "text_report"  in st.session_state
voice_done = "voice_report" in st.session_state
st.markdown(_progress_html(text_done, voice_done), unsafe_allow_html=True)

# ══════════════════════════════════════════════
# ROUND 1 — TEXT INTERVIEW
# ══════════════════════════════════════════════
st.markdown("###  Round 1 — Text interview")

if "questions" not in st.session_state:
    if st.button("Generate questions", type="primary"):
        with st.spinner("Generating interview questions…"):
            agent    = InterviewAgent()
            response = agent.generate_questions(
                candidate_profile={
                    "candidate_name": candidate_name,
                    "strengths":      default_strengths
                },
                role=role,
                num_questions=3
            )
            st.session_state["questions"] = response["questions"]
        st.rerun()

if "questions" in st.session_state and "text_report" not in st.session_state:
    answers = []
    for i, question in enumerate(st.session_state["questions"]):
        with st.container(border=True):
            st.markdown(
                f"<div style='font-size:12px; font-weight:600; color:#888;"
                f"            text-transform:uppercase; letter-spacing:0.05em;"
                f"            margin-bottom:4px;'>Question {i + 1}</div>"
                f"<div style='font-size:15px; color:#1A1A2E;"
                f"            margin-bottom:10px;'>{question}</div>",
                unsafe_allow_html=True
            )
            answer = st.text_area(
                "Your answer",
                key=f"answer_{i}",
                height=100,
                placeholder="Type your answer here…"
            )
            answers.append(answer)

    if st.button("Submit text round →", type="primary"):
        if not all(a.strip() for a in answers):
            st.warning("Please answer all questions before submitting.")
        else:
            with st.spinner("Evaluating answers…"):
                agent       = InterviewAgent()
                evaluations = [
                    agent.evaluate_answer(q, a)
                    for q, a in zip(st.session_state["questions"], answers)
                ]
                text_report = agent.generate_interview_report(evaluations)
                st.session_state["text_report"] = text_report
            st.rerun()

# ─────────────────────────────────────────────
# Text round result
# ─────────────────────────────────────────────
if "text_report" in st.session_state:
    text_report = st.session_state["text_report"]
    text_score  = text_report.get("overall_score", 0)

    with st.container(border=True):
        st.markdown("**Text round result**")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Overall score",      text_score)
        m2.metric("Technical",          text_report.get("average_technical_score", 0))
        m3.metric("Communication",      text_report.get("average_communication_score", 0))
        m4.metric("Accuracy",           text_report.get("average_accuracy_score", 0))

    if text_score >= 70:
        st.success(f" Text round cleared (score: {text_score}). Proceeding to voice round.")
    else:
        st.error(
            f" Text round score {text_score} is below the pass threshold (70). "
            "Candidate cannot proceed to the voice round."
        )
        st.stop()

# ══════════════════════════════════════════════
# ROUND 2 — VOICE INTERVIEW (only after text pass)
# ══════════════════════════════════════════════
if "text_report" in st.session_state and "voice_report" not in st.session_state:
    st.divider()
    st.markdown("###  Round 2 — Voice interview")

    st.info(
        "Camera monitoring starts automatically when you begin the voice round. "
        "Make sure your microphone and camera are accessible."
    )

    if st.button("▶ Start proctored voice interview", type="primary"):
        # ── Guard: only start one proctoring thread ──
        if not st.session_state.get("proctoring_active", False):
            agent     = InterviewAgent()
            voice     = VoiceAgent()
            tts       = TTSAgent()
            proctor   = ProctoringAgent()

            monitor_thread        = threading.Thread(
                target=proctor.start_monitoring,
                daemon=True
            )
            monitor_thread.start()
            st.session_state["proctoring_active"] = True
            st.success("AI proctoring started.")

            response = agent.generate_questions(
                candidate_profile={
                    "candidate_name": candidate_name,
                    "strengths":      default_strengths
                },
                role=role,
                num_questions=2
            )
            voice_questions = response["questions"]
            voice_evals     = []

            for i, question in enumerate(voice_questions, start=1):
                with st.container(border=True):
                    st.markdown(
                        f"<div style='font-size:12px; font-weight:600; color:#888;"
                        f"            text-transform:uppercase; margin-bottom:4px;'>"
                        f"  Voice question {i}</div>"
                        f"<div style='font-size:15px; color:#1A1A2E;'>{question}</div>",
                        unsafe_allow_html=True
                    )
                    tts.speak(question)

                    with st.spinner(f"Recording answer for question {i}…"):
                        transcript = voice.record_and_transcribe()

                    st.success(f'Answer recorded: \u201c{transcript}\u201d')

                    evaluation = agent.evaluate_answer(question, transcript)
                    voice_evals.append(evaluation)

            proctor.stop_monitoring()
            st.session_state["proctoring_active"] = False

            voice_report = agent.generate_interview_report(voice_evals)
            risk_report  = proctor.get_risk_score()

            st.session_state["voice_report"] = voice_report
            st.session_state["risk_report"]  = risk_report

            st.success("Voice round complete!")
            st.rerun()

# ══════════════════════════════════════════════
# FINAL REPORT — save + display
# ══════════════════════════════════════════════
if (
    "text_report"  in st.session_state
    and "voice_report" in st.session_state
    and "risk_report"  in st.session_state
):
    st.divider()
    st.markdown("###  Final interview report")

    text_report  = st.session_state["text_report"]
    voice_report = st.session_state["voice_report"]
    risk_report  = st.session_state["risk_report"]

    text_score   = text_report.get("overall_score", 0)
    voice_score  = voice_report.get("overall_score", 0)
    risk_score   = risk_report.get("risk_score", 0)

    final_score = round(
        (text_score + voice_score) / 2 - (risk_score * 0.2),
        2
    )
    recommendation = "Proceed" if final_score >= 70 else "Reject"

    # ── Metrics ───────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Text score",  text_score)
    c2.metric("Voice score", voice_score)
    c3.metric("Risk score",  risk_score)
    c4.metric("Final score", final_score)

    if recommendation == "Proceed":
        st.success(" Recommended for HR review")
    else:
        st.error(" Not recommended — below pass threshold")

    # ── Save report ───────────────────────────
    os.makedirs("data/reports", exist_ok=True)
    report_data = {
        "candidate_name": candidate_name,
        "text_score":     text_score,
        "voice_score":    voice_score,
        "risk_score":     risk_score,
        "final_score":    final_score,
        "recommendation": recommendation,
        "text_report":    text_report,
        "voice_report":   voice_report,
        "risk_report":    risk_report
    }

    report_json = json.dumps(report_data, indent=4)

    with open("data/reports/interview_report.json", "w", encoding="utf-8") as fh:
        json.dump(report_data, fh, indent=4)

    b1, b2 = st.columns([2, 6])
    with b1:
        if st.button(" View full report →", type="primary"):
            st.switch_page("pages/4_Interview_Report.py")
    with b2:
        st.download_button(
            "⬇ Download report JSON",
            data=report_json,
            file_name="interview_report.json",
            mime="application/json"
        )