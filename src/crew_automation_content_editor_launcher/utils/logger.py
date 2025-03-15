import logging
import os
import sys
import time
from datetime import datetime

class ContentEditorLogger:
    """
    A comprehensive logging system for the Content Editor System.
    Logs all agent activities, inputs, outputs, and data access with timestamps.
    """
    
    def __init__(self, log_level=logging.INFO, log_file=None):
        """
        Initialize the logger with the specified log level and file.
        
        Args:
            log_level: The logging level (default: logging.INFO)
            log_file: The path to the log file (default: None, generates a timestamped file)
        """
        self.logger = logging.getLogger("ContentEditorSystem")
        self.logger.setLevel(log_level)
        self.logger.handlers = []
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Create console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # Create file handler if log_file is provided or generate a timestamped one
        if log_file is None:
            log_dir = os.path.join(os.getcwd(), 'logs')
            os.makedirs(log_dir, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_file = os.path.join(log_dir, f"content_editor_{timestamp}.log")
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        
        self.log_info(f"Logger initialized. Log file: {log_file}")
    
    def log_debug(self, message):
        """Log a debug message."""
        self.logger.debug(message)
    
    def log_info(self, message):
        """Log an info message."""
        self.logger.info(message)
    
    def log_warning(self, message):
        """Log a warning message."""
        self.logger.warning(message)
    
    def log_error(self, message):
        """Log an error message."""
        self.logger.error(message)
    
    def log_critical(self, message):
        """Log a critical message."""
        self.logger.critical(message)
    
    def log_agent_action(self, agent_name, action, details=None):
        """Log an agent action with details."""
        message = f"AGENT: {agent_name} | ACTION: {action}"
        if details:
            message += f" | DETAILS: {details}"
        self.log_info(message)
    
    def log_task_execution(self, task_name, agent_name, status, details=None):
        """Log a task execution with status and details."""
        message = f"TASK: {task_name} | AGENT: {agent_name} | STATUS: {status}"
        if details:
            message += f" | DETAILS: {details}"
        self.log_info(message)
    
    def log_data_access(self, agent_name, data_source, operation, details=None):
        """Log data access operations (read/write) with details."""
        message = f"DATA ACCESS: {agent_name} | SOURCE: {data_source} | OPERATION: {operation}"
        if details:
            message += f" | DETAILS: {details}"
        self.log_info(message)
    
    def log_input_output(self, agent_name, input_data=None, output_data=None):
        """Log agent input and output data."""
        if input_data:
            self.log_info(f"INPUT: {agent_name} | DATA: {input_data}")
        if output_data:
            self.log_info(f"OUTPUT: {agent_name} | DATA: {output_data}")
    
    def log_api_call(self, api_name, endpoint, status, details=None):
        """Log API calls with status and details."""
        message = f"API CALL: {api_name} | ENDPOINT: {endpoint} | STATUS: {status}"
        if details:
            message += f" | DETAILS: {details}"
        self.log_info(message)
    
    def log_workflow_step(self, step_name, status, details=None):
        """Log workflow steps with status and details."""
        message = f"WORKFLOW: {step_name} | STATUS: {status}"
        if details:
            message += f" | DETAILS: {details}"
        self.log_info(message)

# Create a singleton instance
logger = ContentEditorLogger()