import json
import requests
from langchain.tools import tool
from config import SERPER_API_KEY

class SearchTools:
    @tool("Search the internet")
    def search_internet(self, query):
        """Useful to search the internet about a given topic and return relevant results"""
        top_result_to_return = 4
        url = "https://google.serper.dev/search"
        payload = json.dumps({"q": query})
        headers = {
            'X-API-KEY': SERPER_API_KEY,
            'content-type': 'application/json'
        }
        
        try:
            response = requests.request("POST", url, headers=headers, data=payload)
            results = response.json()
            
            if 'organic' not in results:
                return "Sorry, I couldn't find anything about that. There might be an issue with the search API."
                
            string = []
            for result in results['organic'][:top_result_to_return]:
                try:
                    string.append('\n'.join([
                        f"Title: {result['title']}",
                        f"Link: {result['link']}",
                        f"Snippet: {result['snippet']}",
                        "\n-----------------"
                    ]))
                except KeyError:
                    continue
                    
            return '\n'.join(string)
            
        except Exception as e:
            return f"Error searching internet: {str(e)}"
