from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import os
import json
import requests
import backoff
from ..utils.logger import logger
from ..utils.config_manager import ConfigManager

class WebSearchToolInput(BaseModel):
    """Input schema for WebSearchTool."""
    query: str = Field(..., description="The search query to perform.")
    num_results: int = Field(5, description="The number of search results to return.")

class WebSearchTool(BaseTool):
    name: str = "Web Search Tool"
    description: str = (
        "Search the web for information using the Serper API."
    )
    args_schema: Type[BaseModel] = WebSearchToolInput
    api_key: str = Field(default_factory=lambda: os.getenv("SERPER_API_KEY") or ConfigManager().get_api_key("serper"))

    def _run(self, query: str, num_results: int = 5) -> str:
        # Input validation
        if not query or not isinstance(query, str):
            error_msg = "Invalid search query: must be a non-empty string"
            logger.log_error(error_msg)
            return error_msg
            
        if not isinstance(num_results, int) or not (1 <= num_results <= 100):
            error_msg = f"Invalid num_results: {num_results}. Must be between 1-100"
            logger.log_error(error_msg)
            return error_msg

        if not self.api_key:
            error_msg = "Missing Serper API key - check configuration"
            logger.log_error(error_msg)
            return error_msg

        logger.log_agent_action("WebSearchTool", "search", f"Searching for '{query}' on the web")
        
        try:
            url = "https://google.serper.dev/search"
            payload = json.dumps({
                "q": query,
                "num": num_results,
                "page": 1,
                "hl": "en"
            })
            headers = {
                'X-API-KEY': self.api_key,
                'Content-Type': 'application/json',
                'User-Agent': 'CrewAI/1.0 (Siebert_Content_Crew)'
            }
            
            @backoff.on_exception(backoff.expo,
                              requests.exceptions.RequestException,
                              max_tries=3)
            @backoff.on_predicate(backoff.expo,
                               lambda r: r.status_code >= 500,
                               max_tries=3)
            def make_request():
                logger.log_api_call("Serper API", "search", "pending", f"Query: {query}")
                return requests.request("POST", url, headers=headers, data=payload)
            
            response = make_request()
            
            if response.status_code == 403:
                error_msg = "Invalid or missing API credentials - verify ConfigManager settings"
                logger.log_error(error_msg)
                return f"ERROR: {error_msg}. Please check your API configuration."

            if response.status_code != 200:
                error_msg = f"API request failed: {response.status_code} - {response.text}"
                logger.log_error(error_msg)
                return f"ERROR: {error_msg}"

            search_results = response.json()
            
            # Format the results
            result_str = f"## Web Search Results for '{query}'\n\n"
            
            # Process organic results
            if "organic" in search_results:
                result_str += "### Top Results:\n"
                for i, result in enumerate(search_results["organic"], 1):
                    if i > num_results:
                        break
                    
                    title = result.get("title", "No title")
                    link = result.get("link", "No link")
                    snippet = result.get("snippet", "No snippet")
                    date = result.get("date", "Date not available")
                    author = result.get("author", "Unknown author")
                    
                    result_str += f"**{i}. {title}**\n"
                    result_str += f"- 🔗 [Source]({link})\n"
                    result_str += f"- 👤 {author}\n" if author else ""
                    result_str += f"- 📅 {date}\n" if date else ""
                    result_str += f"- 📝 {snippet}\n\n"
            
            # Process knowledge graph
            if "knowledgeGraph" in search_results:
                kg = search_results["knowledgeGraph"]
                result_str += "\n### Knowledge Graph:\n"
                result_str += f"**{kg.get('title', 'N/A')}**\n"
                result_str += f"- Type: {kg.get('type', 'N/A')}\n"
                result_str += f"- Description: {kg.get('description', 'N/A')}\n"
                
                for attr, value in kg.get('attributes', {}).items():
                    result_str += f"- {attr.capitalize()}: {value}\n"
            
            logger.log_info(f"Found {min(num_results, len(search_results.get('organic', [])))} search results for '{query}'")
            return result_str
        
        except Exception as e:
            error_msg = f"Error searching the web: {str(e)}"
            logger.log_error(error_msg)
            return error_msg