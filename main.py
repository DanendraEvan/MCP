import streamlit as st
from MCPclient import MCPClient

class ResearchAppClient:
    def __init__(self):
        self.client = MCPClient()
        self._setup_ui()
        
    def _display_paper_info(self, paper_info: dict):
        """Display paper information in Streamlit format"""
        st.subheader(paper_info['title'])
        st.write(f"**Authors:** {', '.join(paper_info['authors'])}")
        st.write(f"**Published:** {paper_info['published']}")
        st.markdown("---")
        st.subheader("Abstract")
        st.write(paper_info['summary'])
        st.markdown(f"[Download PDF]({paper_info['pdf_url']})", unsafe_allow_html=True)

    def _setup_ui(self):
        """Set up the Streamlit user interface"""
        st.set_page_config(page_title="Research Assistant", layout="wide")
        st.title("Research Assistant Chatbot")
        
        # Main input area
        user_input = st.text_input(
            "Ask a research question or enter a paper ID (e.g., 2401.12345):",
            placeholder="Your question or paper ID..."
        )
        
        if st.button("Submit") and user_input:
            with st.spinner("Processing your request..."):
                # Check if input looks like a paper ID
                if any(c.isdigit() for c in user_input):
                    # Try to get paper info
                    paper_info = self.client.send_request("extract_info", {"paper_id": user_input})
                    if 'error' in paper_info:
                        # If not found locally, try to fetch from arXiv
                        paper_info = self.client.send_request("get_paper_content", {"paper_id": user_input})
                    
                    if 'error' not in paper_info:
                        self._display_paper_info(paper_info)
                        return
                
                # Default research assistant response
                response = self.client.send_request("research_assistant", {"query": user_input})
                result = response.get('response', response.get('error', 'No response available'))
                
                st.subheader("Research Assistant Response")
                st.markdown(result)
        
        # API functions section
        st.markdown("---")
        st.subheader("API Functions")
        
        with st.expander("Search Papers"):
            topic = st.text_input("Research topic:")
            max_results = st.number_input("Max results:", min_value=1, max_value=20, value=5)
            if st.button("Search Papers"):
                with st.spinner("Searching papers..."):
                    result = self.client.send_request("search_papers", {
                        "topic": topic,
                        "max_results": max_results
                    })
                    st.json(result)
        
        with st.expander("Get Paper Content"):
            paper_id = st.text_input("Paper ID:")
            if st.button("Get Paper Content"):
                with st.spinner("Fetching paper..."):
                    result = self.client.send_request("get_paper_content", {"paper_id": paper_id})
                    st.json(result)
        
        with st.expander("Research Assistant API"):
            query = st.text_input("Research question:")
            if st.button("Ask Research Assistant"):
                with st.spinner("Generating response..."):
                    result = self.client.send_request("research_assistant", {"query": query})
                    st.json(result)

if __name__ == "__main__":
    app = ResearchAppClient()
