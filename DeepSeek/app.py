import streamlit as st
from research_assistant import ResearchAssistant
from dotenv import load_dotenv
import os
from datetime import datetime

# Load API key
load_dotenv()
API_KEY = os.getenv("API_KEY")

# Initialize assistant
if API_KEY is None:
    st.error("API_KEY not found. Please set it in your environment variables.")
    st.stop()
assistant = ResearchAssistant(api_key=API_KEY)

# Streamlit UI
st.set_page_config(page_title="AI Research Assistant", layout="wide")
st.title("🤖 AI Research Assistant")
st.markdown("Ask a research question and get a comprehensive, sourced answer.")

# Sidebar input
st.sidebar.header("Settings")
question = st.sidebar.text_area("Enter your research question:", height=120)
run_button = st.sidebar.button("Start Research")

if run_button:
    if not question.strip():
        st.warning("⚠️ Please enter a research question.")
    else:
        with st.spinner("🔍 Researching... please wait."):
            results = assistant.research_question(question)

        # Show summary
        st.subheader("📌 Research Summary")
        st.text(results['summary'])

        # Show detailed analysis
        st.subheader("📖 Detailed Analysis")
        st.markdown(results['answer'])

        # Show logs in expander
        with st.expander("📜 Detailed Research Logs"):
            st.text(results['detailed_logs'])

        # Show sources
        st.subheader("🔗 Sources")
        for step in results["research_log"]:
            for src in step["key_sources"]:
                st.markdown(f"- [{src['title']}]({src['url']})")

        # Download option
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"research_results_{timestamp}.txt"
        file_content = f"{results['summary']}\n\n{results['answer']}\n\n{results['detailed_logs']}"
        st.download_button("📥 Download Results", file_content, file_name=filename)
