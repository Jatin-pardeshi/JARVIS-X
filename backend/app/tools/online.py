import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
from typing import Dict, Any
from app.tools.base import BaseTool

class WebSearchTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="web_search",
            description="Searches the internet for information using DuckDuckGo. Pass a 'query' parameter.",
            required_permissions=["execute_url"]
        )

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        query = params.get("query")
        if not query:
            return {"status": "error", "message": "Missing required parameter 'query'"}

        try:
            results = []
            with DDGS() as ddgs:
                for r in ddgs.text(query, max_results=5):
                    results.append({
                        "title": r.get("title", ""),
                        "href": r.get("href", ""),
                        "body": r.get("body", "")
                    })
            return {
                "status": "success",
                "data": results
            }
        except Exception as e:
            return {"status": "error", "message": f"Web search failed: {str(e)}"}

class WebScraperTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="web_scraper",
            description="Fetches and extracts text content from a specified URL. Pass a 'url' parameter.",
            required_permissions=["read_url"]
        )

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        url = params.get("url")
        if not url:
            return {"status": "error", "message": "Missing required parameter 'url'"}

        try:
            # Set a reasonable timeout and a user-agent to avoid immediate blocking
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.extract()

            text = soup.get_text(separator=' ')
            
            # Collapse whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)

            # Limit text to avoid blowing up context window (e.g. 10,000 characters)
            max_chars = 10000
            if len(text) > max_chars:
                text = text[:max_chars] + "\n...[CONTENT TRUNCATED]..."

            return {
                "status": "success",
                "data": text
            }
        except requests.exceptions.Timeout:
            return {"status": "error", "message": f"Request to {url} timed out."}
        except requests.exceptions.RequestException as e:
            return {"status": "error", "message": f"Network error when fetching {url}: {str(e)}"}
        except Exception as e:
            return {"status": "error", "message": f"Web scraping failed: {str(e)}"}
