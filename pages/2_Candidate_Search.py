import streamlit as st

from agents.qdrant_agent import QdrantAgent

st.set_page_config(
    page_title="Candidate Search · RecruitAI",
    page_icon="",
    layout="wide"
)

# ─────────────────────────────────────────────
# Page header
# ─────────────────────────────────────────────
st.markdown(
    "<h2 style='margin-bottom:0.25rem;'> Candidate Search</h2>"
    "<p style='color:#666; margin-bottom:1.5rem;'>"
    "Semantic search across all screened candidates stored in Qdrant.</p>",
    unsafe_allow_html=True
)

# ─────────────────────────────────────────────
# Search controls
# ─────────────────────────────────────────────
search_col, limit_col = st.columns([4, 1], gap="medium")

with search_col:
    query = st.text_input(
        "Search query",
        placeholder="e.g. Machine Learning engineer with NLP and Python experience",
        label_visibility="collapsed"
    )

with limit_col:
    limit = st.selectbox(
        "Results",
        options=[5, 10, 15, 20],
        index=0,
        label_visibility="collapsed"
    )

# ── Filter pills ──────────────────────────────
st.markdown(
    "<div style='display:flex; gap:6px; flex-wrap:wrap; margin-bottom:1.25rem;'>"
    "  <span style='font-size:12px; color:#888; align-self:center;'>Filters:</span>"
    "  <span style='font-size:12px; background:#EEEDFE; color:#3C3489;"
    "               border:1px solid #E0DFF8; padding:3px 12px;"
    "               border-radius:20px; cursor:pointer;'>All</span>"
    "  <span style='font-size:12px; background:#F5F5F5; color:#555;"
    "               border:1px solid #E5E5E5; padding:3px 12px;"
    "               border-radius:20px; cursor:pointer;'>Score ≥ 80</span>"
    "  <span style='font-size:12px; background:#F5F5F5; color:#555;"
    "               border:1px solid #E5E5E5; padding:3px 12px;"
    "               border-radius:20px; cursor:pointer;'>Recommended only</span>"
    "  <span style='font-size:12px; background:#F5F5F5; color:#555;"
    "               border:1px solid #E5E5E5; padding:3px 12px;"
    "               border-radius:20px; cursor:pointer;'>AI / ML</span>"
    "</div>",
    unsafe_allow_html=True
)

search_btn = st.button(
    " Search candidates",
    type="primary",
    disabled=not query.strip()
)

if not query.strip():
    st.info("Enter a search query above to find matching candidates.")
    st.stop()

# ─────────────────────────────────────────────
# Search + results
# ─────────────────────────────────────────────
if search_btn:
    with st.spinner("Searching…"):
        try:
            qdrant  = QdrantAgent()
            results = qdrant.search_candidates(query=query, limit=limit)
        except Exception as err:
            st.error(f"Search failed: {err}")
            st.stop()

    if not results:
        st.warning(
            "No matching candidates found. "
            "Try broadening your query or screen more resumes first."
        )
        st.stop()

    st.markdown(
        f"<p style='font-size:13px; color:#888; margin-bottom:1rem;'>"
        f"  {len(results)} candidate(s) found for <em>\"{query}\"</em>"
        f"</p>",
        unsafe_allow_html=True
    )

    for idx, result in enumerate(results, start=1):
        candidate  = result.get("candidate", {})
        score      = result.get("score", 0)

        name           = candidate.get("candidate_name", "Unknown")
        cand_score     = candidate.get("candidate_score", 0)
        recommendation = candidate.get("recommendation", "")
        strengths      = candidate.get("strengths", [])
        missing        = candidate.get("missing_skills", [])

        initials = "".join(w[0].upper() for w in name.split()[:2])

        # Score colour
        if cand_score >= 80:
            score_color = "#27500A"
        elif cand_score >= 60:
            score_color = "#3C3489"
        else:
            score_color = "#D85A30"

        with st.container(border=True):
            top_left, top_right = st.columns([5, 2])

            with top_left:
                st.markdown(
                    f"<div style='display:flex; align-items:center; gap:10px;'>"
                    f"  <div style='width:38px; height:38px; border-radius:50%;"
                    f"              background:#EEEDFE; color:#3C3489;"
                    f"              font-size:13px; font-weight:600;"
                    f"              display:flex; align-items:center;"
                    f"              justify-content:center; flex-shrink:0;'>{initials}</div>"
                    f"  <div>"
                    f"    <div style='font-size:15px; font-weight:600;'>{name}</div>"
                    f"    <div style='font-size:12px; color:#888;'>"
                    f"      Similarity score: {round(score, 3)}</div>"
                    f"  </div>"
                    f"</div>",
                    unsafe_allow_html=True
                )

            with top_right:
                st.markdown(
                    f"<div style='text-align:right;'>"
                    f"  <div style='font-size:24px; font-weight:700;"
                    f"              color:{score_color};'>{cand_score}</div>"
                    f"  <div style='font-size:11px; color:#999;'>candidate score</div>"
                    f"</div>",
                    unsafe_allow_html=True
                )

            # Progress bar
            st.markdown(
                f"<div style='height:5px; border-radius:3px; background:#EBEBEB;"
                f"            margin:10px 0;'>"
                f"  <div style='height:100%; border-radius:3px; width:{cand_score}%;"
                f"              background:{score_color};'></div>"
                f"</div>",
                unsafe_allow_html=True
            )

            s_col, m_col = st.columns(2)

            with s_col:
                if strengths:
                    pills = "".join(
                        f"<span class='pill pill-green'>{s}</span>"
                        for s in strengths
                    )
                    st.markdown(
                        f"<div style='font-size:12px; color:#555;"
                        f"            font-weight:600; margin-bottom:4px;'>Strengths</div>"
                        f"<div class='pill-row'>{pills}</div>",
                        unsafe_allow_html=True
                    )

            with m_col:
                if missing:
                    pills = "".join(
                        f"<span class='pill pill-amber'>{s}</span>"
                        for s in missing
                    )
                    st.markdown(
                        f"<div style='font-size:12px; color:#555;"
                        f"            font-weight:600; margin-bottom:4px;'>Missing skills</div>"
                        f"<div class='pill-row'>{pills}</div>",
                        unsafe_allow_html=True
                    )

            if recommendation:
                st.caption(f" {recommendation}")

            # ── Action buttons ─────────────────────
            b1, b2, _ = st.columns([2, 2, 4])
            with b1:
                if st.button(
                    " Start interview",
                    key=f"iv_{idx}_{name}"
                ):
                    st.session_state["interview_candidate_name"] = name
                    st.session_state["interview_strengths"] = strengths
                    st.switch_page("pages/3_Interview_Center.py")
            with b2:
                if st.button(
                    " View report",
                    key=f"rpt_{idx}_{name}"
                ):
                    st.switch_page("pages/4_Interview_Report.py")


# ─────────────────────────────────────────────
# Scoped CSS
# ─────────────────────────────────────────────
st.markdown(
    """
    <style>
    .pill-row  {display:flex; flex-wrap:wrap; gap:6px; margin-top:4px;}
    .pill      {display:inline-block; font-size:12px; padding:3px 10px;
                border-radius:20px; border:1px solid #E0DFF8;
                color:#3C3489; background:#EEEDFE;}
    .pill-green{background:#EAF3DE; color:#27500A; border-color:#C0DD97;}
    .pill-amber{background:#FAEEDA; color:#633806; border-color:#FAC775;}
    </style>
    """,
    unsafe_allow_html=True
)
