import streamlit as st
import streamlit.components.v1 as components
from agents.search_agent import SearchAgent
from agents.analysis_agent import AnalysisAgent
from config import STREAMLIT_THEME

# Configure Streamlit page
st.set_page_config(
    page_title="Document Search Assistant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom theme
st.markdown("""
<style>
    .stApp {
        background-color: white;
    }
    .stSidebar {
        background-color: #F0F2F6;
    }
    .stTextInput {
        background-color: white;
    }
</style>
""", unsafe_allow_html=True)

# Custom navbar HTML
navbar_html = """
<nav style="
    background-color: #262730;
    padding: 1rem;
    position: fixed;
    width: 100%;
    top: 0;
    left: 0;
    z-index: 999;
    display: flex;
    justify-content: space-between;
    align-items: center;
">
    <div style="color: white; font-size: 1.5rem;">📚 Document Search Assistant</div>
    <div>
        <a href="#" style="color: white; text-decoration: none; margin: 0 1rem;">Home</a>
        <a href="#" style="color: white; text-decoration: none; margin: 0 1rem;">About</a>
        <a href="#" style="color: white; text-decoration: none; margin: 0 1rem;">Help</a>
    </div>
</nav>
<div style="margin-top: 4rem;"></div>
"""

# Display navbar
st.markdown(navbar_html, unsafe_allow_html=True)

# Initialize session state
if 'search_history' not in st.session_state:
    st.session_state.search_history = []

# Sidebar
with st.sidebar:
    st.title("Settings")
    language = st.selectbox("Select Language", ["English", "Hindi", "Urdu"])
    st.divider()
    st.subheader("Search History")
    for query in st.session_state.search_history:
        st.text(query)

# Main content
st.title("Document Search Assistant")

# Search input
query = st.text_input("Enter your search query:")
search_button = st.button("Search")

if search_button and query:
    st.session_state.search_history.append(query)
    
    with st.spinner("Searching for documents..."):
        # Initialize agents
        search_agent = SearchAgent()
        analysis_agent = AnalysisAgent()
        
        # Perform search
        search_results = search_agent.search(query)
        
        # Analyze results
        analysis_results = analysis_agent.analyze(search_results)
        
        # Display results
        st.subheader("Search Results")
        try:
            results = eval(search_results)
            for doc in results.get('documents', []):
                with st.expander(doc['title']):
                    st.write(f"**Relevance:** {doc['relevance']}")
                    st.write("**Key Points:**")
                    for point in doc['key_points']:
                        st.write(f"- {point}")
                    st.write(f"[View Document]({doc['url']})")
        except:
            st.write(search_results)
            
        st.subheader("Analysis")
        try:
            analysis = eval(analysis_results)
            with st.expander("Requirements"):
                for req in analysis['analysis']['requirements']:
                    st.write(f"- {req}")
            
            with st.expander("Process Steps"):
                for step in analysis['analysis']['process_steps']:
                    st.write(f"- {step}")
                    
            with st.expander("Additional Resources"):
                for resource in analysis['analysis']['additional_resources']:
                    st.write(f"- {resource}")
        except:
            st.write(analysis_results)

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit")
