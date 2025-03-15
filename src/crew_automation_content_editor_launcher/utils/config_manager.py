import os
import json
from typing import Dict, Any, Optional
from .logger import logger

class ConfigManager:
    """
    Manages configuration settings for the Content Editor System.
    Handles API keys, model selection, and other configuration parameters.
    """
    
    def __init__(self):
        """
        Initialize the Configuration Manager with default settings.
        """
        # Default API keys (will be overridden by environment variables if available)
        self.api_keys = {
            "serper": os.getenv("SERPER_API_KEY", ""),
            "anthropic": os.getenv("ANTHROPIC_API_KEY", ""),
            "openai": os.getenv("OPENAI_API_KEY", "")
        }
        
        # Default model settings for each agent
        self.agent_models = {
            "leader": "anthropic",  # Using Claude by default
            "web_searcher": "openai",  # Using GPT by default
            "copywriter": "anthropic",  # Using Claude by default
            "editor": "openai"  # Using GPT by default
        }
        
        # Set environment variables for API keys if not already set
        self._set_environment_variables()
        
        logger.log_info("Config Manager initialized with default settings")
    
    def _set_environment_variables(self):
        """
        Set environment variables for API keys if not already set.
        """
        # Only set environment variables if they don't already exist
        if not os.getenv("SERPER_API_KEY") and self.api_keys["serper"]:
            os.environ["SERPER_API_KEY"] = self.api_keys["serper"]
        
        if not os.getenv("ANTHROPIC_API_KEY") and self.api_keys["anthropic"]:
            os.environ["ANTHROPIC_API_KEY"] = self.api_keys["anthropic"]
        
        if not os.getenv("OPENAI_API_KEY") and self.api_keys["openai"]:
            os.environ["OPENAI_API_KEY"] = self.api_keys["openai"]
        
        logger.log_info("Environment variables checked for API keys")
    
    def get_api_key(self, service_name):
        service_name = service_name.lower()
        if service_name == 'serper':
            return os.getenv('SERPER_API_KEY')
        elif service_name == 'anthropic':
            return os.getenv('ANTHROPIC_API_KEY')
        elif service_name == 'openai':
            return os.getenv('OPENAI_API_KEY')
        else:
            raise ValueError(f"Unsupported service: {service_name}")
    
    def set_api_key(self, provider: str, api_key: str):
        """
        Set the API key for the specified provider.
        
        Args:
            provider: The provider name (serper, anthropic, or openai)
            api_key: The API key to set
        """
        self.api_keys[provider] = api_key
        self._set_environment_variables()
        
        logger.log_info(f"API key updated for provider: {provider}")
    
    def get_agent_model(self, agent_name: str) -> str:
        """
        Get the model provider for the specified agent.
        
        Args:
            agent_name: The name of the agent
            
        Returns:
            The model provider for the specified agent (anthropic or openai)
        """
        if agent_name not in self.agent_models:
            logger.log_error(f"Model not found for agent: {agent_name}")
            return "openai"  # Default to OpenAI if not found
        
        return self.agent_models[agent_name]
    
    def set_agent_model(self, agent_name: str, model_provider: str):
        """
        Set the model provider for the specified agent.
        
        Args:
            agent_name: The name of the agent
            model_provider: The model provider to set (anthropic or openai)
        """
        if model_provider not in ["anthropic", "openai"]:
            logger.log_error(f"Invalid model provider: {model_provider}. Must be 'anthropic' or 'openai'.")
            return
        
        self.agent_models[agent_name] = model_provider
        logger.log_info(f"Model provider updated for agent: {agent_name} -> {model_provider}")
    
    def save_config(self, config_file: str = "config.json"):
        """
        Save the current configuration to a JSON file.
        
        Args:
            config_file: The path to the configuration file
        """
        config = {
            "api_keys": self.api_keys,
            "agent_models": self.agent_models
        }
        
        try:
            with open(config_file, "w") as f:
                json.dump(config, f, indent=4)
            
            logger.log_info(f"Configuration saved to {config_file}")
        except Exception as e:
            logger.log_error(f"Error saving configuration: {str(e)}")
    
    def load_config(self, config_file: str = "config.json"):
        """
        Load configuration from a JSON file.
        
        Args:
            config_file: The path to the configuration file
        """
        try:
            with open(config_file, "r") as f:
                config = json.load(f)
            
            if "api_keys" in config:
                self.api_keys = config["api_keys"]
            
            if "agent_models" in config:
                self.agent_models = config["agent_models"]
            
            self._set_environment_variables()
            
            logger.log_info(f"Configuration loaded from {config_file}")
        except Exception as e:
            logger.log_error(f"Error loading configuration: {str(e)}")

# Create a singleton instance
config_manager = ConfigManager()