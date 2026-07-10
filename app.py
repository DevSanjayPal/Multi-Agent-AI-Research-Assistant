import streamlit as st
from pipeline import research_pipeline

# ----------------------------
# Page Configuration
# ----------------------------
st.set_page_config(
    page_title="Research System with Agents",
    page_icon="🤖",
    layout="wide"
)

# ----------------------------
# Title
# ----------------------------
st.title("🤖 Research System with Agents")
st.markdown(
    """
Enter any research topic and let the AI agents:

- 🔍 Search the web
- 📖 Read & Scrape content
- ✍️ Generate a research report
- 🧐 Critique the report
"""
)

st.divider()

# ----------------------------
# Input
# ----------------------------
topic = st.text_input(
    "Enter Research Topic",
    placeholder="Example: Artificial Intelligence in Healthcare"
)

# ----------------------------
# Button
# ----------------------------
if st.button("🚀 Start Research", use_container_width=True):

    if topic.strip() == "":
        st.warning("Please enter a research topic.")
        st.stop()

    with st.spinner("Agents are working..."):

        try:
            result = research_pipeline(topic)

            st.success("Research Completed!")

            # ----------------------------
            # Search Results
            # ----------------------------
            with st.expander("🔍 Search Results", expanded=False):
                st.write(result.get("s_results", "No search results."))

            # ----------------------------
            # Scraped Content
            # ----------------------------
            with st.expander("📖 Scraped Content", expanded=False):
                st.write(result.get("scraped_result", "No scraped content."))

            # ----------------------------
            # Final Report
            # ----------------------------
            st.subheader("📄 Final Research Report")
            st.write(result.get("report", "No report generated."))

            # ----------------------------
            # Critic Feedback
            # ----------------------------
            st.subheader("🧐 Critic Feedback")
            st.write(result.get("feedback", "No feedback generated."))

        except Exception as e:
            st.error(f"Error: {e}")