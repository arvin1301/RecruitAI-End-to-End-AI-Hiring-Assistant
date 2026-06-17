import streamlit as st

st.set_page_config(
    page_title="RecruitAI",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# Global CSS — shared across all pages
# ─────────────────────────────────────────────
st.markdown(
    """
    <style>
    /* Sidebar nav */
    [data-testid="stSidebarNav"] {display: none;}

    /* Suppress default Streamlit padding */
    .block-container {padding-top: 1.5rem;}

    /* Metric cards */
    div[data-testid="metric-container"] {
        background: #F7F7FB;
        border: 1px solid #E8E7F8;
        border-radius: 10px;
        padding: 1rem 1.25rem;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 8px;
        font-weight: 500;
        font-size: 0.875rem;
    }

    /* Primary action button override */
    .stButton > button[kind="primary"] {
        background: #3C3489;
        border: none;
    }

    /* Info, success, warning, error boxes */
    .stAlert {border-radius: 8px;}

    /* Sidebar branding */
    section[data-testid="stSidebar"] {
        background: #FAFAFA;
        border-right: 1px solid #EBEBEB;
    }

    /* Divider */
    hr {border-color: #EBEBEB; margin: 1.25rem 0;}

    /* Pill tags */
    .pill-row {display: flex; flex-wrap: wrap; gap: 6px; margin-top: 6px;}
    .pill {
        display: inline-block;
        font-size: 12px;
        padding: 3px 10px;
        border-radius: 20px;
        border: 1px solid #E0DFF8;
        color: #3C3489;
        background: #EEEDFE;
    }
    .pill-green {
        background: #EAF3DE;
        color: #27500A;
        border-color: #C0DD97;
    }
    .pill-amber {
        background: #FAEEDA;
        color: #633806;
        border-color: #FAC775;
    }

    /* Candidate row */
    .cand-row {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 10px 0;
        border-bottom: 1px solid #F0F0F0;
    }
    .avatar {
        width: 36px; height: 36px;
        border-radius: 50%;
        background: #EEEDFE;
        color: #3C3489;
        font-size: 13px;
        font-weight: 600;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }

    /* Score bar */
    .score-bar-bg {
        height: 6px;
        border-radius: 3px;
        background: #EBEBEB;
        overflow: hidden;
        margin-top: 4px;
    }
    .score-bar-fill {
        height: 100%;
        border-radius: 3px;
        background: #534AB7;
    }

    /* Step tracker */
    .step-row {
        display: flex;
        align-items: flex-start;
        gap: 10px;
        padding: 10px 0;
        border-bottom: 1px solid #F0F0F0;
    }
    .step-row:last-child {border-bottom: none;}
    .step-icon {
        width: 30px; height: 30px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 14px;
        flex-shrink: 0;
    }
    .step-done {background: #EAF3DE; color: #27500A;}
    .step-active {background: #EEEDFE; color: #3C3489;}
    .step-pending {background: #F5F5F5; color: #AAAAAA;}

    /* Section label */
    .section-label {
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.07em;
        text-transform: uppercase;
        color: #999;
        margin-bottom: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ─────────────────────────────────────────────
# Sidebar navigation
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        """
        <div style="display:flex; align-items:center; gap:10px;
                    padding: 0.5rem 0 1.5rem;">
            <span style="font-size:22px;"></span>
            <span style="font-size:16px; font-weight:600;
                         color:#1A1A2E;">RecruitAI</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.page_link("app.py",               label="Home",             )
    st.page_link("pages/1_Resume_Screening.py",  label="Resume Screening" )
    st.page_link("pages/2_Candidate_Search.py",  label="Candidate Search" )
    st.page_link("pages/3_Interview_Center.py",  label="Interview Center" )
    st.page_link("pages/4_Interview_Report.py",  label="Interview Report" )
    st.page_link("pages/5_HR_Dashboard.py",      label="HR Dashboard"     )

    st.divider()
    st.caption("Platform v2.0 · Powered by AI")


# ─────────────────────────────────────────────
# Home page content
# ─────────────────────────────────────────────
st.markdown(
    "<h2 style='margin-bottom:0.25rem;'>Welcome back </h2>"
    "<p style='color:#666; margin-bottom:1.5rem;'>"
    "Here's a snapshot of your hiring pipeline.</p>",
    unsafe_allow_html=True
)

# ── KPI row ──────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
c1.metric("Resumes reviewed",    "142", "+18 this week")
c2.metric("Shortlisted",         "34",  "24% rate")
c3.metric("Interviews done",     "21",  "3 in progress")
c4.metric("Offers extended",     "6",   "4 accepted")

st.divider()

# ── Pipeline stages + recent candidates ──────
left, right = st.columns([1, 1], gap="large")

with left:
    st.markdown(
        "<div class='section-label'>Pipeline stages</div>",
        unsafe_allow_html=True
    )
    stages = [
        ("done",    "✓",  "Resume screening",  "142 resumes processed",  " Done"),
        ("done",    "✓",  "Text interviews",   "34 candidates assessed", " Done"),
        ("active",  "🎤", "Voice interviews",  "21 of 34 completed",     " Active"),
        ("pending", "👤", "HR review",         "Pending",                ""),
    ]
    html = "<div>"
    for state, icon, title, sub, badge in stages:
        icon_class = f"step-{state}"
        html += (
            f"<div class='step-row'>"
            f"  <div class='step-icon {icon_class}'>{icon}</div>"
            f"  <div style='flex:1'>"
            f"    <div style='font-size:14px; font-weight:500;'>{title}</div>"
            f"    <div style='font-size:12px; color:#888;'>{sub}</div>"
            f"  </div>"
            f"  <span style='font-size:12px; color:#666;'>{badge}</span>"
            f"</div>"
        )
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)

with right:
    st.markdown(
        "<div class='section-label'>Recent candidates</div>",
        unsafe_allow_html=True
    )
    candidates = [
        ("AS", "Arvind Sharma",  "AI Engineer",       87, "#534AB7", " Proceed"),
        ("PK", "Priya Kapoor",   "ML Engineer",       74, "#0F6E56", " Review"),
        ("RN", "Rohit Nair",     "Backend Engineer",  51, "#D85A30", " Reject"),
    ]
    html = "<div>"
    for initials, name, role, score, color, rec in candidates:
        pct = score
        html += (
            f"<div class='cand-row'>"
            f"  <div class='avatar'>{initials}</div>"
            f"  <div style='flex:1'>"
            f"    <div style='font-size:14px; font-weight:500;'>{name}</div>"
            f"    <div style='font-size:12px; color:#888;'>{role}</div>"
            f"    <div class='score-bar-bg'>"
            f"      <div class='score-bar-fill'"
            f"           style='width:{pct}%; background:{color};'></div>"
            f"    </div>"
            f"  </div>"
            f"  <span style='font-size:12px; white-space:nowrap;'>{rec}</span>"
            f"</div>"
        )
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)

st.divider()
st.info(
    "Use the sidebar to navigate. "
    "Start with **Resume Screening** to evaluate a new candidate."
)
