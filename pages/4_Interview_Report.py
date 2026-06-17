import os
import json

import streamlit as st

st.set_page_config(
    page_title="Interview Report · RecruitAI",
    page_icon="",
    layout="wide"
)

# ─────────────────────────────────────────────
# Page header
# ─────────────────────────────────────────────
st.markdown(
    "<h2 style='margin-bottom:0.25rem;'> Interview Report</h2>"
    "<p style='color:#666; margin-bottom:1.5rem;'>"
    "Full breakdown of the candidate's text, voice, and proctoring scores.</p>",
    unsafe_allow_html=True
)

# ─────────────────────────────────────────────
# Load report
# ─────────────────────────────────────────────
REPORT_PATH = "data/reports/interview_report.json"

if not os.path.exists(REPORT_PATH):
    st.warning(
        "No interview report found. "
        "Complete an interview first in the Interview Center."
    )
    if st.button("Go to Interview Center →"):
        st.switch_page("pages/3_Interview_Center.py")
    st.stop()

with open(REPORT_PATH, "r", encoding="utf-8") as fh:
    report = json.load(fh)

candidate_name  = report.get("candidate_name",  "Unknown")
text_score      = report.get("text_score",      0)
voice_score     = report.get("voice_score",     0)
risk_score      = report.get("risk_score",      0)
final_score     = report.get("final_score",     0)
recommendation  = report.get("recommendation",  "N/A")
text_report     = report.get("text_report",     {})
voice_report    = report.get("voice_report",    {})
risk_report     = report.get("risk_report",     {})

initials = "".join(w[0].upper() for w in candidate_name.split()[:2])

# ─────────────────────────────────────────────
# Candidate header
# ─────────────────────────────────────────────
with st.container(border=True):
    hdr_left, hdr_right = st.columns([5, 2])

    with hdr_left:
        st.markdown(
            f"<div style='display:flex; align-items:center; gap:12px;'>"
            f"  <div style='width:48px; height:48px; border-radius:50%;"
            f"              background:#EEEDFE; color:#3C3489;"
            f"              font-size:16px; font-weight:600;"
            f"              display:flex; align-items:center;"
            f"              justify-content:center; flex-shrink:0;'>{initials}</div>"
            f"  <div>"
            f"    <div style='font-size:18px; font-weight:600;'>{candidate_name}</div>"
            f"    <div style='font-size:13px; color:#888;'>Interview report</div>"
            f"  </div>"
            f"</div>",
            unsafe_allow_html=True
        )

    with hdr_right:
        if recommendation == "Proceed":
            st.success("Recommended for HR review")
        else:
            st.error("Not recommended")

# ─────────────────────────────────────────────
# KPI metrics
# ─────────────────────────────────────────────
st.divider()
m1, m2, m3, m4 = st.columns(4)
m1.metric("Text score",  text_score)
m2.metric("Voice score", voice_score)
m3.metric("Risk score",  risk_score,  delta_color="inverse")
m4.metric("Final score", final_score)

# ─────────────────────────────────────────────
# Score breakdown — side-by-side
# ─────────────────────────────────────────────
st.divider()
st.markdown("#### Score breakdown")

def _score_row(label: str, value: float, color: str = "#534AB7") -> str:
    pct = min(max(int(value), 0), 100)
    return (
        f"<div style='display:flex; align-items:center; gap:10px; padding:8px 0;"
        f"            border-bottom:1px solid #F0F0F0;'>"
        f"  <span style='font-size:13px; flex:1;'>{label}</span>"
        f"  <div style='width:120px; height:6px; border-radius:3px;"
        f"              background:#EBEBEB; overflow:hidden;'>"
        f"    <div style='height:100%; border-radius:3px; width:{pct}%;"
        f"                background:{color};'></div>"
        f"  </div>"
        f"  <span style='font-size:13px; font-weight:600; min-width:28px;"
        f"               text-align:right;'>{value}</span>"
        f"</div>"
    )

left, right = st.columns(2, gap="large")

with left:
    with st.container(border=True):
        st.markdown(
            "<div style='font-size:12px; font-weight:600; color:#888;"
            "            text-transform:uppercase; margin-bottom:8px;'>"
            "Text interview</div>",
            unsafe_allow_html=True
        )
        st.markdown(
            _score_row("Technical accuracy",
                       text_report.get("average_technical_score", 0))
            + _score_row("Communication",
                         text_report.get("average_communication_score", 0))
            + _score_row("Answer accuracy",
                         text_report.get("average_accuracy_score", 0)),
            unsafe_allow_html=True
        )

with right:
    with st.container(border=True):
        st.markdown(
            "<div style='font-size:12px; font-weight:600; color:#888;"
            "            text-transform:uppercase; margin-bottom:8px;'>"
            "Voice interview</div>",
            unsafe_allow_html=True
        )
        st.markdown(
            _score_row("Technical accuracy",
                       voice_report.get("average_technical_score", 0),
                       "#0F6E56")
            + _score_row("Communication",
                         voice_report.get("average_communication_score", 0),
                         "#0F6E56")
            + _score_row("Answer accuracy",
                         voice_report.get("average_accuracy_score", 0),
                         "#0F6E56"),
            unsafe_allow_html=True
        )

# ─────────────────────────────────────────────
# Proctoring report
# ─────────────────────────────────────────────
st.divider()
st.markdown("#### AI proctoring report")

phone_events    = risk_report.get("phone_events",           0)
multi_events    = risk_report.get("multiple_person_events", 0)
missing_events  = risk_report.get("missing_person_events",  0)

def _risk_badge(count: int) -> str:
    if count == 0:
        return (
            "<span style='font-size:12px; background:#EAF3DE; color:#27500A;"
            "             border:1px solid #C0DD97; padding:3px 10px;"
            "             border-radius:20px; font-weight:600;'>0 events</span>"
        )
    return (
        f"<span style='font-size:12px; background:#FAEEDA; color:#633806;"
        f"             border:1px solid #FAC775; padding:3px 10px;"
        f"             border-radius:20px; font-weight:600;'>{count} event(s)</span>"
    )

proctor_html = (
    "<div style='border:1px solid #EBEBEB; border-radius:10px; overflow:hidden;'>"
    + "".join(
        f"<div style='display:flex; align-items:center; justify-content:space-between;"
        f"            padding:12px 16px; border-bottom:1px solid #F0F0F0;'>"
        f"  <span style='font-size:14px;'>{icon}  {label}</span>"
        f"  {_risk_badge(count)}"
        f"</div>"
        for icon, label, count in [
            ("📱", "Phone detected",        phone_events),
            ("👥", "Multiple persons",      multi_events),
            ("🚶", "Candidate left frame",  missing_events),
        ]
    )
    + "</div>"
)

with st.container():
    p_col, tip_col = st.columns([3, 2], gap="large")
    with p_col:
        st.markdown(proctor_html, unsafe_allow_html=True)
    with tip_col:
        total_flags = phone_events + multi_events + missing_events
        if total_flags == 0:
            st.success("No proctoring flags. Clean session.")
        elif total_flags <= 2:
            st.warning(
                f"{total_flags} minor flag(s) detected. "
                "Review timestamps before proceeding."
            )
        else:
            st.error(
                f"{total_flags} proctoring flags. "
                "High-risk session — recommend re-interview."
            )

# ─────────────────────────────────────────────
# Hiring readiness
# ─────────────────────────────────────────────
st.divider()
st.markdown("#### Hiring readiness")

if final_score >= 85:
    st.success(" Excellent candidate — fast-track to offer stage.")
elif final_score >= 70:
    st.info(" Good candidate — recommended for HR review.")
elif final_score >= 60:
    st.warning("⚠ Borderline candidate — requires closer review.")
else:
    st.error(" Weak candidate — does not meet the bar.")

# ─────────────────────────────────────────────
# Recruiter notes
# ─────────────────────────────────────────────
st.divider()
st.markdown("#### Recruiter notes")

# Pre-load saved notes if they exist
notes_path    = "data/recruiter_notes/recruiter_notes.txt"
existing_notes = ""
if os.path.exists(notes_path):
    with open(notes_path, "r", encoding="utf-8") as fh:
        existing_notes = fh.read()

notes = st.text_area(
    "Add notes for the hiring team",
    value=existing_notes,
    height=120,
    placeholder="e.g. Strong Python skills, needs FastAPI coaching, cultural fit confirmed…"
)

n1, n2 = st.columns([2, 6])
with n1:
    if st.button(" Save notes", type="primary"):
        os.makedirs("data/recruiter_notes", exist_ok=True)
        with open(notes_path, "w", encoding="utf-8") as fh:
            fh.write(notes)
        st.success("Notes saved.")

with n2:
    if st.button("👤 Send to HR Dashboard →"):
        st.switch_page("pages/5_HR_Dashboard.py")
