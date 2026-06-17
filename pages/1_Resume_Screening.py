import os
import json
from pathlib import Path

import streamlit as st

from agents.resume_parser import ResumeParser
from agents.recruiter_agent import RecruiterAgent
from agents.qdrant_agent import QdrantAgent

st.set_page_config(
    page_title="Resume Screening · RecruitAI",
    page_icon="",
    layout="wide"
)

# ─────────────────────────────────────────────
# Page header
# ─────────────────────────────────────────────
st.markdown(
    "<h2 style='margin-bottom:0.25rem;'> Resume Screening</h2>"
    "<p style='color:#666; margin-bottom:1.5rem;'>"
    "Upload a resume and evaluate it against a job description. "
    "Screened candidates are automatically saved to the search index.</p>",
    unsafe_allow_html=True
)

# ─────────────────────────────────────────────
# Default job description
# ─────────────────────────────────────────────
DEFAULT_JD = """\
Role: AI Engineer

Required Skills:
- Python
- FastAPI
- LangChain
- Vector Databases
- LLMs

Experience: 0–2 Years
"""

# ─────────────────────────────────────────────
# Layout — upload + JD on left, result on right
# ─────────────────────────────────────────────
left, right = st.columns([1, 1], gap="large")

with left:
    st.markdown("#### Upload resume")
    uploaded_files = st.file_uploader(
        "Drag and drop PDF or DOCX files here",
        type=["pdf", "docx"],
        accept_multiple_files=True,
        help="Select one or more resumes to screen in a single run."
    )

    st.markdown("#### Job description")
    job_description = st.text_area(
        "Paste or edit the job description",
        value=DEFAULT_JD,
        height=220
    )

    evaluate_btn = st.button(
        "Evaluate candidates",
        type="primary",
        disabled=not uploaded_files
    )

# ─────────────────────────────────────────────
# Evaluation logic
# ─────────────────────────────────────────────
with right:
    if not uploaded_files:
        st.info("Upload at least one resume on the left to get started.")

    elif evaluate_btn:
        os.makedirs("resumes", exist_ok=True)
        os.makedirs("data/reports", exist_ok=True)

        recruiter = RecruiterAgent()
        qdrant    = QdrantAgent()
        results   = []

        progress = st.progress(0, text="Preparing…")

        for idx, uploaded_file in enumerate(uploaded_files):
            # ── Sanitize filename ─────────────────
            safe_filename = Path(uploaded_file.name).name
            file_path     = os.path.join("resumes", safe_filename)

            with open(file_path, "wb") as fh:
                fh.write(uploaded_file.getbuffer())

            progress.progress(
                (idx + 0.4) / len(uploaded_files),
                text=f"Parsing {safe_filename}…"
            )

            try:
                resume_text = ResumeParser.extract_text(file_path)

                progress.progress(
                    (idx + 0.7) / len(uploaded_files),
                    text=f"Evaluating {safe_filename}…"
                )

                result = recruiter.evaluate_candidate(
                    resume_text=resume_text,
                    job_description=job_description
                )
                results.append((safe_filename, result))

                # ── Persist report ────────────────
                candidate_name = result.get("candidate_name", "Unknown")
                safe_name = (
                    candidate_name
                    .replace(" ", "_")
                    .replace("/", "_")
                    .replace("\\", "_")
                )
                report_path = f"data/reports/{safe_name}_resume_result.json"
                with open(report_path, "w", encoding="utf-8") as fh:
                    json.dump(result, fh, indent=4, ensure_ascii=False)

                # ── Upsert to Qdrant so search works ──
                try:
                    qdrant.upsert_candidate(result)
                except Exception as qerr:
                    st.warning(
                        f"Saved report but could not index {candidate_name} "
                        f"in Qdrant: {qerr}"
                    )

                # ── Persist to session for Interview page ──
                st.session_state["last_resume_result"] = result

            except Exception as err:
                st.error(f"Error processing {safe_filename}: {err}")
                continue

        progress.progress(1.0, text="Done!")

        # ─────────────────────────────────────────
        # Display results
        # ─────────────────────────────────────────
        for safe_filename, result in results:
            candidate_name  = result.get("candidate_name", "Unknown")
            candidate_score = result.get("candidate_score", 0)
            strengths       = result.get("strengths", [])
            missing_skills  = result.get("missing_skills", [])
            recommendation  = result.get("recommendation", "")

            initials = "".join(
                w[0].upper()
                for w in candidate_name.split()[:2]
            )

            # Score colour
            if candidate_score >= 80:
                score_color = "#27500A"
                score_bg    = "#EAF3DE"
            elif candidate_score >= 60:
                score_color = "#3C3489"
                score_bg    = "#EEEDFE"
            else:
                score_color = "#712B13"
                score_bg    = "#FAECE7"

            # ── Candidate card ─────────────────────
            with st.container(border=True):
                header_col, score_col = st.columns([4, 1])

                with header_col:
                    st.markdown(
                        f"<div style='display:flex; align-items:center; gap:10px;'>"
                        f"  <div style='width:40px; height:40px; border-radius:50%;"
                        f"              background:#EEEDFE; color:#3C3489;"
                        f"              font-size:14px; font-weight:600;"
                        f"              display:flex; align-items:center;"
                        f"              justify-content:center;'>{initials}</div>"
                        f"  <div>"
                        f"    <div style='font-size:16px; font-weight:600;'>"
                        f"      {candidate_name}</div>"
                        f"    <div style='font-size:12px; color:#888;'>"
                        f"      {safe_filename}</div>"
                        f"  </div>"
                        f"</div>",
                        unsafe_allow_html=True
                    )

                with score_col:
                    st.markdown(
                        f"<div style='text-align:right;'>"
                        f"  <span style='font-size:28px; font-weight:700;"
                        f"               color:{score_color};'>"
                        f"    {candidate_score}"
                        f"  </span>"
                        f"  <span style='font-size:13px; color:#999;'> / 100</span>"
                        f"</div>",
                        unsafe_allow_html=True
                    )

                # Score progress bar
                st.markdown(
                    f"<div style='height:6px; border-radius:3px;"
                    f"            background:#EBEBEB; margin:8px 0 14px;'>"
                    f"  <div style='height:100%; border-radius:3px; width:{candidate_score}%;"
                    f"              background:{score_color};'></div>"
                    f"</div>",
                    unsafe_allow_html=True
                )

                s_col, m_col = st.columns(2)

                with s_col:
                    st.markdown("**Strengths**")
                    if strengths:
                        pills_html = "<div class='pill-row'>" + "".join(
                            f"<span class='pill pill-green'>{s}</span>"
                            for s in strengths
                        ) + "</div>"
                        st.markdown(pills_html, unsafe_allow_html=True)
                    else:
                        st.caption("None identified")

                with m_col:
                    st.markdown("**Missing skills**")
                    if missing_skills:
                        pills_html = "<div class='pill-row'>" + "".join(
                            f"<span class='pill pill-amber'>{s}</span>"
                            for s in missing_skills
                        ) + "</div>"
                        st.markdown(pills_html, unsafe_allow_html=True)
                    else:
                        st.caption("None — full match!")

                st.info(f" {recommendation}")

                # ── Action buttons ─────────────────
                btn1, btn2, _ = st.columns([2, 2, 3])
                with btn1:
                    if st.button(
                        " Start interview",
                        key=f"interview_{candidate_name}",
                        help="Open the Interview Center pre-filled for this candidate"
                    ):
                        st.session_state["interview_candidate_name"] = candidate_name
                        st.session_state["interview_strengths"] = strengths
                        st.switch_page("pages/3_Interview_Center.py")

                with btn2:
                    st.download_button(
                        "⬇ Download report",
                        data=json.dumps(result, indent=4, ensure_ascii=False),
                        file_name=f"{safe_name}_resume_result.json",
                        mime="application/json",
                        key=f"dl_{candidate_name}"
                    )

    # ── Empty right panel until evaluated ─────
    elif uploaded_files and not evaluate_btn:
        st.markdown(
            f"<div style='padding:2rem; text-align:center; color:#888;'>"
            f"  <div style='font-size:32px; margin-bottom:8px;'></div>"
            f"  <div>{len(uploaded_files)} file(s) ready — "
            f"click <strong>Evaluate candidates</strong> to begin.</div>"
            f"</div>",
            unsafe_allow_html=True
        )

# ─────────────────────────────────────────────
# Inline CSS (scoped to this page)
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
