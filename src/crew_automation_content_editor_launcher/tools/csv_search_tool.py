from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import os
import pandas as pd
from crew_automation_content_editor_launcher.utils.logger import logger
from ..utils.csv_manager import CSVManager, CSVManagerConfig

class CSVSearchToolInput(BaseModel):
    """Input schema for CSVSearchTool."""
    csv_file: str = Field(..., description="The CSV file to search in (brand_info, best_practices, or compliance_info).")
    query: str = Field(..., description="The query to search for in the CSV file.")
    
    class Config:
        arbitrary_types_allowed = True

class CSVSearchTool(BaseTool):
    name: str = "CSV Search Tool"
    description: str = (
        "Search for information in the RAG CSV files (brand_info, best_practices, or compliance_info)."
    )
    args_schema: Type[BaseModel] = CSVSearchToolInput
    csv_manager: CSVManager = None
    
    class Config:
        arbitrary_types_allowed = True
    
    def __init__(self):
        super().__init__()
        self.csv_manager = CSVManager()
        logger.log_info("CSV Search Tool initialized")
    
    def _run(self, csv_file: str, query: str) -> str:
        logger.log_agent_action("CSVSearchTool", "search", f"Searching for '{query}' in {csv_file}")
        
        try:
            # Load the appropriate CSV file
            if csv_file.lower() == "brand_info":
                data = self.csv_manager.load_brand_info()
            elif csv_file.lower() == "best_practices":
                data = self.csv_manager.load_best_practices()
            elif csv_file.lower() == 'compliance_info':
                data = self.csv_manager.load_compliance_info()
            else:
                warning_msg = f"Warning: Invalid CSV file '{csv_file}'. Valid options are: brand_info, best_practices, compliance_info"
                logger.log_warning(warning_msg)
                return warning_msg
            
            # Search for the query in the data
            
            # Split query into terms for partial matching
            query_terms = query.lower().split()
            results = {}
            for key, value in data.items():
                key_lower = key.lower()
                value_str = str(value).lower()
                for term in query_terms:
                    if term in key_lower or term in value_str:
                        results[key] = value
                        break
            
            if not results:
                logger.log_warning(f"No results found for '{query}' in {csv_file}. Try broader terms.")
                return f"Warning: No exact matches found. Consider using different search terms."
            
            # Format the results
            result_str = f"Found {len(results)} related entries for '{query}' in {csv_file}:\n"
            for key, value in results.items():
                result_str += f"- {key}: {value}\n"
            
            logger.log_info(f"Found {len(results)} results for '{query}' in {csv_file}")
            return result_str
        
        except Exception as e:
            error_msg = f"Error searching CSV file: {str(e)}"
            logger.log_error(error_msg)
            return error_msg