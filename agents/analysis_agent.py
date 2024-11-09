from crewai import Agent
from langchain.llms import OpenAI  # Ensure you import the correct class
from config import CEREBRAS_API_KEY, CEREBRAS_API_BASE, ANALYSIS_AGENT_MODEL

class AnalysisAgent:
    def __init__(self):
        self.client = OpenAI(
            model=ANALYSIS_AGENT_MODEL["model"],
            temperature=ANALYSIS_AGENT_MODEL["temperature"],
            max_tokens=ANALYSIS_AGENT_MODEL["max_tokens"],
            api_key=CEREBRAS_API_KEY,
            base_url=CEREBRAS_API_BASE
        )
        
        self.agent = Agent(
            role='Content Analyzer',
            goal='Analyze and extract key information from documents',
            backstory="You're an expert at analyzing documents and extracting structured information.",
            llm=self.client,  # Pass the client instance directly
            verbose=True
        )
    
    def analyze(self, content):
        task = self.agent.create_task(
            description=f"Analyze the following content and extract key information:\n\n{content}",
            expected_output="Structured JSON with analysis results and key points"
        )
        return task.execute()
     