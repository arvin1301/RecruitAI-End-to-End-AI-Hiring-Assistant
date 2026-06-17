import streamlit as st
import os
import sys
import importlib.util

st.set_page_config(
    page_title="AI Recruitment Platform",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .stAlert {
        border-radius: 10px;
        border-left: 4px solid;
    }

    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: bold;
    }

    .stButton button {
        border-radius: 20px;
        transition: all 0.3s ease;
        width: 100%;
    }

    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }

    .stAlert {
        animation: slideIn 0.3s ease-out;
    }

    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.history = []
    st.session_state.user_preferences = {}
    st.session_state.total_candidates = 0
    st.session_state.interviews_completed = 0

st.title("🤖 AI Recruitment Platform")
st.caption("Intelligent Hiring Assistant powered by AI")

# Sidebar Navigation
st.sidebar.title("📋 Navigation")

# Navigation options
pages = {
    "📄 Resume Screening": {
        "icon": "📄",
        "description": "Upload and evaluate resumes against job descriptions",
        "file": "1_Resume_Screening.py"
    },
    "🔍 Candidate Search": {
        "icon": "🔍",
        "description": "Semantic search through candidate database",
        "file": "2_Candidate_Search.py"
    },
    "🎤 Interview Center": {
        "icon": "🎤",
        "description": "Conduct AI-powered interviews",
        "file": "3_Interview_Center.py"
    },
    "📊 Interview Report": {
        "icon": "📊",
        "description": "View detailed interview analytics",
        "file": "4_Interview_Report.py"
    },
    "👨‍💼 HR Dashboard": {
        "icon": "👨‍💼",
        "description": "HR decision-making and candidate management",
        "file": "5_HR_Dashboard.py"
    }
}

# Create selection
selected_page = st.sidebar.radio(
    "Select Module",
    options=list(pages.keys()),
    format_func=lambda x: f"{pages[x]['icon']} {x}",
    label_visibility="collapsed"
)

# Show description
st.sidebar.markdown("---")
st.sidebar.info(f"**ℹ️ {selected_page}**\n\n{pages[selected_page]['description']}")

# Quick guide
st.sidebar.markdown("---")
with st.sidebar.expander("📚 Quick Guide"):
    st.markdown("""
    **Workflow:**
    1. 📄 Upload resume for screening
    2. 🎤 Conduct AI interview if qualified  
    3. 📊 Review detailed reports
    4. 👨‍💼 Make HR decisions
    """)

# System status
st.sidebar.markdown("---")
status_col1, status_col2 = st.sidebar.columns(2)
with status_col1:
    st.markdown("🟢 System")
    st.caption("Online")
with status_col2:
    st.markdown("🔐 Secure")
    st.caption("SSL Enabled")

# Quick stats
st.sidebar.markdown("---")
st.sidebar.markdown("**📊 Quick Stats**")
st.sidebar.metric("Total Candidates", st.session_state.total_candidates)
st.sidebar.metric("Interviews", st.session_state.interviews_completed)

# Welcome metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Candidates", st.session_state.total_candidates, delta="Awaiting Upload")
with col2:
    st.metric("Interviews Completed", st.session_state.interviews_completed, delta="Ready to Start")
with col3:
    success_rate = 0 if st.session_state.interviews_completed == 0 else (st.session_state.interviews_completed / max(1,
                                                                                                                     st.session_state.total_candidates)) * 100
    st.metric("Success Rate", f"{success_rate:.0f}%", delta="Based on completed")

st.markdown("---")


# Function to load module dynamically
def load_module(file_path):
    """Load and execute a Python module from file path"""
    try:
        if os.path.exists(file_path):
            # Read and execute the file
            with open(file_path, 'r', encoding='utf-8') as file:
                code = file.read()
                exec(code, globals())
            return True
        else:
            st.error(f"❌ Module file '{file_path}' not found.")
            st.info("📁 Please ensure all page files are in the same directory as app.py")

            # Show current directory for debugging
            st.write(f"**Current directory:** {os.getcwd()}")
            st.write("**Available files:**")
            files = [f for f in os.listdir('.') if f.endswith('.py')]
            for f in files:
                st.write(f"- {f}")

            return False
    except Exception as e:
        st.error(f"❌ Error loading module: {str(e)}")
        return False


# Load the selected page
page_file = pages[selected_page]["file"]
load_module(page_file)

# Footer
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.caption("🤖 AI Recruitment Platform v2.0 | Powered by Streamlit")
    st.caption("© 2024 | Secure & Compliant")