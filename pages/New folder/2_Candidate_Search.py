import streamlit as st
import pandas as pd
from datetime import datetime

from agents.qdrant_agent import QdrantAgent

st.set_page_config(
    page_title="Candidate Search",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 Semantic Candidate Search")
st.write("Search candidates stored in Qdrant using natural language queries.")

# Sidebar filters
with st.sidebar:
    st.header("🔍 Search Filters")

    min_score = st.slider("Minimum Similarity Score", 0.0, 1.0, 0.0, 0.05)
    date_range = st.date_input(
        "Application Date Range",
        value=(datetime.now().replace(month=1, day=1), datetime.now())
    )

    skills_filter = st.multiselect(
        "Required Skills",
        ["Python", "Machine Learning", "Deep Learning", "NLP", "FastAPI",
         "LangChain", "Vector Databases", "LLMs", "Computer Vision", "SQL"]
    )

    experience_filter = st.select_slider(
        "Experience Range (Years)",
        options=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        value=(0, 5)
    )

    st.markdown("---")
    st.caption("💡 Tip: Use natural language queries like 'Machine Learning Engineer with NLP experience'")

# Main search area
query = st.text_input(
    "🔎 Search Query",
    placeholder="Example: Senior Python developer with FastAPI and LLM experience",
    help="Enter a natural language description of the ideal candidate"
)

col1, col2 = st.columns([3, 1])
with col1:
    limit = st.slider("Number of Results", min_value=1, max_value=50, value=10)
with col2:
    search_button = st.button("🔍 Search Candidates", type="primary", use_container_width=True)

if search_button:
    if not query.strip():
        st.warning("⚠️ Please enter a search query.")
    else:
        with st.spinner("🔍 Searching candidate database..."):
            try:
                qdrant = QdrantAgent()

                results = qdrant.search_candidates(
                    query=query,
                    limit=limit
                )

                if not results:
                    st.warning("❌ No matching candidates found.")
                    st.info("💡 Try broadening your search query or adjusting filters.")
                else:
                    # Filter results by min_score
                    filtered_results = [r for r in results if r["score"] >= min_score]

                    st.success(f"✅ Found {len(filtered_results)} matching candidates")

                    # Display results count
                    st.metric("Total Results", len(filtered_results),
                              delta=f"Out of {len(results)} total")

                    # Display results in expandable cards
                    for index, result in enumerate(filtered_results, start=1):
                        with st.expander(f"**Candidate {index}** - Score: {result['score']:.3f}",
                                         expanded=(index == 1)):
                            col1, col2 = st.columns([3, 1])

                            with col1:
                                candidate = result["candidate"]

                                st.markdown(f"**Name:** {candidate.get('candidate_name', 'Unknown')}")
                                st.markdown(f"**Overall Score:** {candidate.get('candidate_score', 0)}/100")
                                st.markdown(f"**Recommendation:** {candidate.get('recommendation', 'N/A')}")

                                # Skills sections
                                strengths = candidate.get("strengths", [])
                                missing = candidate.get("missing_skills", [])

                                if strengths:
                                    st.markdown("**✅ Strengths:**")
                                    for skill in strengths[:5]:  # Limit to top 5
                                        st.markdown(f"• {skill}")

                                if missing and len(missing) > 0:
                                    st.markdown("**⚠️ Missing Skills:**")
                                    for skill in missing[:3]:  # Show top 3 missing
                                        st.markdown(f"• {skill}")

                            with col2:
                                st.metric("Similarity Score", f"{result['score']:.3f}")

                                # Quick actions
                                if st.button(f"📊 View Details", key=f"view_{index}"):
                                    st.session_state.selected_candidate = candidate
                                    st.info("Candidate details loaded")

                                if st.button(f"📧 Contact", key=f"contact_{index}"):
                                    st.success("Contact request sent!")

                    # Export results
                    st.markdown("---")
                    st.subheader("📊 Export Results")
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("📥 Export to CSV", use_container_width=True):
                            # Convert results to DataFrame
                            df_data = []
                            for r in filtered_results:
                                candidate = r["candidate"]
                                df_data.append({
                                    "Name": candidate.get("candidate_name", "Unknown"),
                                    "Score": candidate.get("candidate_score", 0),
                                    "Similarity": r["score"],
                                    "Recommendation": candidate.get("recommendation", ""),
                                    "Strengths": ", ".join(candidate.get("strengths", [])[:3])
                                })
                            df = pd.DataFrame(df_data)
                            st.download_button(
                                "Download CSV",
                                df.to_csv(index=False),
                                "candidate_search_results.csv",
                                "text/csv"
                            )
                    with col2:
                        if st.button("💾 Save Search", use_container_width=True):
                            st.success("Search saved to history!")

            except Exception as error:
                st.error(f"❌ Search failed: {str(error)}")
                st.exception(error)

# Recent searches section
if 'search_history' not in st.session_state:
    st.session_state.search_history = []

st.markdown("---")
with st.expander("📜 Recent Searches"):
    if st.session_state.search_history:
        for search in st.session_state.search_history[-5:]:
            st.markdown(f"• {search}")
    else:
        st.info("No recent searches. Start searching to see history here.")