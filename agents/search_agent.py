from crewai import Agent
from tools.search_tools import SearchTools
from tools.browser_tools import BrowserTools
from langchain.llms import OpenAI
from config import GROQ_API_KEY, GROQ_API_BASE, SEARCH_AGENT_MODEL

class SearchAgent:
    def __init__(self):
        self.client = OpenAI(
            model=SEARCH_AGENT_MODEL["model"],
            temperature=SEARCH_AGENT_MODEL["temperature"],
            max_tokens=SEARCH_AGENT_MODEL["max_tokens"],
            api_key=GROQ_API_KEY,
            base_url=GROQ_API_BASE
        )
        
        self.agent = Agent(
            role='Search Specialist',
            goal='Find and retrieve relevant documentation and information',
            backstory="You're an expert at finding and analyzing documentation across multiple domains.",
            tools=[
                SearchTools().search_internet,
                BrowserTools().scrape_and_summarize_website
            ],
            llm=self.client,
            verbose=True
        )
        
    def search(self, query):
        task = self.agent.create_task(
            description=f"Search and analyze documentation for: {query}",
            expected_output="Structured JSON with relevant documents and summaries"
        )
        return task.execute()
