import json
import os
from crewai import Agent, Task
from langchain.tools import tool
from unstructured.partition.html import partition_html
import requests
from config import BROWSERLESS_API_KEY, GROQ_API_BASE, GROQ_API_KEY
import openai

class BrowserTools:
    def __init__(self):
        self.client = openai.OpenAI(
            base_url=GROQ_API_BASE,
            api_key=GROQ_API_KEY
        )

    @tool("Scrape website content")
    def scrape_and_summarize_website(self, website):
        """Useful to scrape and summarize a website content"""
        url = f"https://chrome.browserless.io/content?token={BROWSERLESS_API_KEY}"
        payload = json.dumps({"url": website})
        headers = {'cache-control': 'no-cache', 'content-type': 'application/json'}
        
        try:
            response = requests.request("POST", url, headers=headers, data=payload)
            elements = partition_html(text=response.text)
            content = "\n\n".join([str(el) for el in elements])
            content = [content[i:i + 8000] for i in range(0, len(content), 8000)]
            
            summaries = []
            for chunk in content:
                completion = self.client.chat.completions.create(
                    model="mixtral-8x7b-32768",
                    messages=[{
                        "role": "system",
                        "content": "You are a Principal Researcher tasked with analyzing and summarizing content."
                    }, {
                        "role": "user",
                        "content": f"Analyze and summarize the following content, focusing on the most relevant information:\n\n{chunk}"
                    }]
                )
                summaries.append(completion.choices[0].message.content)
            
            return "\n\n".join(summaries)
            
        except Exception as e:
            return f"Error scraping website: {str(e)}"
