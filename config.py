import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
SERPER_API_KEY = os.getenv('SERPER_API_KEY')
BROWSERLESS_API_KEY = os.getenv('BROWSERLESS_API_KEY')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
CEREBRAS_API_KEY = os.getenv('CEREBRAS_API_KEY')

# API Endpoints
GROQ_API_BASE = "https://api.groq.com/openai/v1"
CEREBRAS_API_BASE = "https://api.cerebras.ai/v1"

# Model configurations
SEARCH_AGENT_MODEL = {
    "model": "llama3-groq-70b-8192-tool-use-preview",  # Groq model
    "temperature": 0.7,
    "max_tokens": 4096
}

ANALYSIS_AGENT_MODEL = {
    "model": "llama3.1-70b",  # Cerebras model
    "temperature": 0.5,
    "max_tokens": 8192
}

# Streamlit configs
STREAMLIT_THEME = {
    "theme": {
        "base": "light",
        "primaryColor": "#FF4B4B",
        "backgroundColor": "#FFFFFF",
        "secondaryBackgroundColor": "#F0F2F6",
        "textColor": "#262730",
        "font": "sans serif"
    }
}
