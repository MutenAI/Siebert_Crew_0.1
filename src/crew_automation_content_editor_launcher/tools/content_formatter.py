from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import os
import re
from ..utils.logger import logger

class ContentFormatterToolInput(BaseModel):
    """Input schema for ContentFormatterTool."""
    content: str = Field(..., description="The content to format.")
    content_type: str = Field("blog", description="The type of content (blog, whitepaper, article, etc.).")
    tone: str = Field(None, description="The tone of voice to use (professional, conversational, etc.).")
    target_audience: str = Field(None, description="The target audience for the content.")
    structure: str = Field(None, description="The structure to follow (intro:problem:solution:conclusion, etc.).")
    include_disclaimers: bool = Field(True, description="Whether to include compliance disclaimers.")

class ContentFormatterTool(BaseTool):
    name: str = "Content Formatter Tool"
    description: str = (
        "Format content according to best practices, structure guidelines, and compliance requirements."
    )
    args_schema: Type[BaseModel] = ContentFormatterToolInput
    
    def __init__(self):
        super().__init__()
        logger.log_info("Content Formatter Tool initialized")
    
    def _run(self, content: str, content_type: str = "blog", tone: str = None, 
             target_audience: str = None, structure: str = None, include_disclaimers: bool = True) -> str:
        logger.log_agent_action("ContentFormatterTool", "format", 
                               f"Formatting {content_type} content with tone: {tone}")
        
        try:
            # Format the content based on the content type and structure
            formatted_content = self._format_content(content, content_type, structure)
            
            # Add appropriate tone adjustments if specified
            if tone:
                formatted_content = self._adjust_tone(formatted_content, tone)
            
            # Add audience-specific elements if specified
            if target_audience:
                formatted_content = self._tailor_to_audience(formatted_content, target_audience)
            
            # Add compliance disclaimers if required
            if include_disclaimers:
                formatted_content = self._add_disclaimers(formatted_content, content_type)
            
            logger.log_info(f"Content formatted successfully for {content_type}")
            return formatted_content
        
        except Exception as e:
            error_msg = f"Error formatting content: {str(e)}"
            logger.log_error(error_msg)
            return error_msg
    
    def _format_content(self, content: str, content_type: str, structure: str = None) -> str:
        """Format the content based on the content type and structure."""
        # Default structure if none provided
        if not structure:
            if content_type.lower() == "blog":
                structure = "introduction:problem:solution:conclusion"
            elif content_type.lower() == "whitepaper":
                structure = "exec_summary:problem:methodology:results:conclusions"
            else:
                structure = "introduction:body:conclusion"
        
        # Split the structure into sections
        sections = structure.split(":")
        
        # If content doesn't already have headers, add them based on structure
        if not re.search(r'#\s+', content):
            formatted_parts = []
            # Split content into roughly equal parts based on number of sections
            content_parts = self._split_content_into_sections(content, len(sections))
            
            for i, section in enumerate(sections):
                section_title = section.replace("_", " ").title()
                if i < len(content_parts):
                    formatted_parts.append(f"## {section_title}\n\n{content_parts[i]}")
                else:
                    formatted_parts.append(f"## {section_title}\n\n")
            
            formatted_content = "\n\n".join(formatted_parts)
        else:
            # Content already has headers, keep as is
            formatted_content = content
        
        return formatted_content
    
    def _split_content_into_sections(self, content: str, num_sections: int) -> list:
        """Split content into roughly equal parts."""
        paragraphs = content.split("\n\n")
        if len(paragraphs) <= num_sections:
            return paragraphs + ["" for _ in range(num_sections - len(paragraphs))]
        
        # Calculate paragraphs per section
        paras_per_section = len(paragraphs) // num_sections
        remainder = len(paragraphs) % num_sections
        
        sections = []
        start_idx = 0
        for i in range(num_sections):
            # Add one extra paragraph to early sections if there's a remainder
            extra = 1 if i < remainder else 0
            end_idx = start_idx + paras_per_section + extra
            section_content = "\n\n".join(paragraphs[start_idx:end_idx])
            sections.append(section_content)
            start_idx = end_idx
        
        return sections
    
    def _adjust_tone(self, content: str, tone: str) -> str:
        """Adjust the tone of the content."""
        # This is a placeholder - in a real implementation, this would use NLP techniques
        # to adjust the tone of the content
        return content
    
    def _tailor_to_audience(self, content: str, audience: str) -> str:
        """Tailor the content to the specified audience."""
        # This is a placeholder - in a real implementation, this would add audience-specific
        # elements to the content
        return content
    
    def _add_disclaimers(self, content: str, content_type: str) -> str:
        """Add appropriate compliance disclaimers based on content type."""
        # Financial services standard disclaimer
        disclaimer = ("\n\n---\n\n*Disclaimer: This content is for informational purposes only and does not "
                    "constitute financial advice. Investment advisory services involve risk. "
                    "Past performance is not indicative of future results. "
                    "Please consult with a qualified financial advisor before making any investment decisions.*")
        
        return content + disclaimer