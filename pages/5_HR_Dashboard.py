import os
import json

import streamlit as st

from agents.hr_agent import HRAgent

st.set_page_config(
    page_title="HR Dashboard · RecruitAI",
    page_icon="",
    layout="wide"
)

# ─────────────────────────────────────────────
# Page header
# ─────────────────────────────────────────────
st.markdown(
    "<h2 style='margin-bottom:0.25rem;'> HR Dashboard</h2>"
    "<p style='color:#666; margin-bottom:1.5rem;'>"
    "Final hiring decision, salary recommendation, and next steps.</p>",
    unsafe_allow_html=True
)

# ─────────────────────────────────────────────
# Load interview report
# ─────────────────────────────────────────────
REPORT_PATH = "data/reports/interview_report.json"

if not os.path.exists(REPORT_PATH):
    st.warning(
        "No interview report found. "
        "Complete an interview first."
    )
    if st.button("Go to Interview Center →"):
        st.switch_page("pages/3_Interview_Center.py")
    st.stop()

with open(REPORT_PATH, "r", encoding="utf-8") as fh:
    interview_report = json.load(fh)

candidate_name = interview_report.get("candidate_name", "Unknown")
final_score    = interview_report.get("final_score",    0)
risk_score     = interview_report.get("risk_score",     0)
recommendation = interview_report.get("recommendation", "Reject")

# Pull actual strengths / missing skills from saved resume result if available
safe_name      = (
    candidate_name
    .replace(" ", "_")
    .replace("/", "_")
    .replace("\\", "_")
)
resume_path    = f"data/reports/{safe_name}_resume_result.json"
resume_strengths  = []
resume_missing    = []

if os.path.exists(resume_path):
    with open(resume_path, "r", encoding="utf-8") as fh:
        resume_result     = json.load(fh)
        resume_strengths  = resume_result.get("strengths",      [])
        resume_missing    = resume_result.get("missing_skills", [])

initials = "".join(w[0].upper() for w in candidate_name.split()[:2])

# ─────────────────────────────────────────────
# Candidate summary card
# ─────────────────────────────────────────────
with st.container(border=True):
    hdr_l, hdr_r = st.columns([4, 2])

    with hdr_l:
        st.markdown(
            f"<div style='display:flex; align-items:center; gap:12px;'>"
            f"  <div style='width:48px; height:48px; border-radius:50%;"
            f"              background:#EEEDFE; color:#3C3489;"
            f"              font-size:16px; font-weight:600;"
            f"              display:flex; align-items:center;"
            f"              justify-content:center; flex-shrink:0;'>{initials}</div>"
            f"  <div>"
            f"    <div style='font-size:18px; font-weight:600;'>{candidate_name}</div>"
            f"    <div style='font-size:13px; color:#888;'>HR evaluation</div>"
            f"  </div>"
            f"</div>",
            unsafe_allow_html=True
        )

    with hdr_r:
        badge = (
            "Recommended"
            if recommendation == "Proceed"
            else "Not recommended"
        )
        if recommendation == "Proceed":
            st.success(badge)
        else:
            st.error(badge)

# ── KPI row ──────────────────────────────────
c1, c2, c3 = st.columns(3)
c1.metric("Final interview score", final_score)
c2.metric("Risk score",            risk_score, delta_color="inverse")
c3.metric("Interview outcome",     recommendation)

# ─────────────────────────────────────────────
# Skills snapshot
# ─────────────────────────────────────────────
if resume_strengths or resume_missing:
    st.divider()
    s_col, m_col = st.columns(2)

    with s_col:
        st.markdown("**Confirmed strengths**")
        if resume_strengths:
            pills = "".join(
                f"<span class='pill pill-green'>{s}</span>"
                for s in resume_strengths
            )
            st.markdown(
                f"<div class='pill-row'>{pills}</div>",
                unsafe_allow_html=True
            )
        else:
            st.caption("No strengths recorded.")

    with m_col:
        st.markdown("**Skill gaps**")
        if resume_missing:
            pills = "".join(
                f"<span class='pill pill-amber'>{s}</span>"
                for s in resume_missing
            )
            st.markdown(
                f"<div class='pill-row'>{pills}</div>",
                unsafe_allow_html=True
            )
        else:
            st.caption("No gaps — full skill match.")

# ─────────────────────────────────────────────
# HR evaluation section
# ─────────────────────────────────────────────
st.divider()
st.markdown("#### Generate HR decision")

if st.button("Run HR evaluation", type="primary"):
    with st.spinner("Running HR evaluation…"):
        hr_agent = HRAgent()

        report_data = {
            "candidate_name":   candidate_name,
            "resume_score":     interview_report.get("text_score",  0),
            "interview_score":  interview_report.get("voice_score", 0),
            "risk_score":       risk_score,
            "final_score":      final_score,
            "resume_strengths": resume_strengths,
            "missing_skills":   resume_missing
        }

        hr_decision = hr_agent.generate_hr_decision(report_data)

        # ── Persist HR report ─────────────────
        os.makedirs("data/hr_reports", exist_ok=True)
        hr_path = f"data/hr_reports/{safe_name}_hr_decision.json"
        with open(hr_path, "w", encoding="utf-8") as fh:
            json.dump(hr_decision, fh, indent=4, ensure_ascii=False)

        st.session_state["hr_decision"] = hr_decision

# ─────────────────────────────────────────────
# Display HR decision
# ─────────────────────────────────────────────
if "hr_decision" in st.session_state:
    hr = st.session_state["hr_decision"]

    status                  = hr.get("status",                  "Unknown")
    salary_band             = hr.get("salary_band",             "N/A")
    next_round              = hr.get("next_round",              "None")
    hr_summary              = hr.get("hr_summary",              "")
    joining_recommendation  = hr.get("joining_recommendation",  "")

    st.divider()
    st.markdown("#### HR decision")

    with st.container(border=True):
        d1, d2, d3 = st.columns(3)
        d1.metric("Status",      status)
        d2.metric("Salary band", salary_band)
        d3.metric("Next round",  next_round)

    # ── Summary + recommendation ──────────────
    sum_col, rec_col = st.columns(2, gap="large")

    with sum_col:
        st.markdown("**HR summary**")
        st.info(hr_summary or "No summary generated.")

    with rec_col:
        st.markdown("**Joining recommendation**")
        if joining_recommendation:
            st.success(joining_recommendation)
        else:
            st.caption("No recommendation provided.")

    # ── Final verdict ─────────────────────────
    st.divider()
    if status.lower() == "selected":
        st.success(
            f"{candidate_name} has been **selected**. "
            "Proceed with offer letter and onboarding."
        )
        if st.button("✉Draft offer letter (opens AI chat)"):
            # Could integrate with a messaging or email agent here
            st.info(
                "Tip: Copy this prompt into your email agent — "
                f"\"Draft an offer letter for {candidate_name} for the role, "
                f"salary band {salary_band}.\""
            )
    else:
        st.error(
            f"{candidate_name} has not been selected at this stage."
        )

    # ── Download HR report ────────────────────
    st.download_button(
        " Download HR decision",
        data=json.dumps(hr, indent=4, ensure_ascii=False),
        file_name=f"{safe_name}_hr_decision.json",
        mime="application/json"
    )

# ─────────────────────────────────────────────
# Recruiter notes (read-only mirror)
# ─────────────────────────────────────────────
notes_path = "data/recruiter_notes/recruiter_notes.txt"
if os.path.exists(notes_path):
    with open(notes_path, "r", encoding="utf-8") as fh:
        notes = fh.read().strip()
    if notes:
        st.divider()
        st.markdown("#### Recruiter notes")
        st.markdown(
            f"<div style='background:#F7F7FB; border:1px solid #E8E7F8;"
            f"            border-radius:8px; padding:12px 16px;"
            f"            font-size:14px; color:#444; line-height:1.6;'>"
            f"  {notes}"
            f"</div>",
            unsafe_allow_html=True
        )

# ─────────────────────────────────────────────
# Scoped CSS
# ─────────────────────────────────────────────
st.markdown(
    """
    <style>
    .pill-row  {display:flex; flex-wrap:wrap; gap:6px; margin-top:6px;}
    .pill      {display:inline-block; font-size:12px; padding:3px 10px;
                border-radius:20px; border:1px solid #E0DFF8;
                color:#3C3489; background:#EEEDFE;}
    .pill-green{background:#EAF3DE; color:#27500A; border-color:#C0DD97;}
    .pill-amber{background:#FAEEDA; color:#633806; border-color:#FAC775;}
    </style>
    """,
    unsafe_allow_html=True
)
