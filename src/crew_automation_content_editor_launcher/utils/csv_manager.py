import os
import csv
import pandas as pd
from typing import Dict, List, Any, Optional
from pydantic import BaseModel
from .logger import logger

class CSVManagerConfig(BaseModel):
    """Configuration for CSVManager to work with Pydantic"""
    class Config:
        arbitrary_types_allowed = True

class CSVManager:
    """
    Manages loading, parsing, and validating CSV files for the Content Editor System.
    Handles the three RAG CSV files: brand_info, best_practices, and compliance_info.
    """
    
    def __init__(self, base_dir: str = None):
        """
        Initialize the CSV Manager with the base directory for RAG files.
        
        Args:
            base_dir: The base directory for RAG files (default: None, uses the current working directory)
        """
        if base_dir is None:
            base_dir = os.path.join(os.getcwd(), 'RAG')
        
        self.base_dir = base_dir
        self.rag1_path = os.path.join(base_dir, 'Rag 1', 'brand_info.csv')
        self.rag2_path = os.path.join(base_dir, 'Rag 2', 'best_practices.csv')
        self.rag3_path = os.path.join(base_dir, 'Rag 3', 'compliance_info.csv - Foglio1.csv')
        
        # Validate that the CSV files exist
        self._validate_csv_files()
        
        logger.log_info(f"CSV Manager initialized with base directory: {base_dir}")
    
    def _validate_csv_files(self):
        """
        Validate that the CSV files exist, and create them if they don't.
        """
        for csv_path, csv_name in [
            (self.rag1_path, "brand_info"),
            (self.rag2_path, "best_practices"),
            (self.rag3_path, "compliance_info")
        ]:
            if not os.path.exists(csv_path):
                logger.log_warning(f"{csv_name} CSV file not found at {csv_path}. Creating a new one.")
                os.makedirs(os.path.dirname(csv_path), exist_ok=True)
                self._create_empty_csv(csv_path, csv_name)
            else:
                logger.log_info(f"{csv_name} CSV file found at {csv_path}")
    
    def _create_empty_csv(self, csv_path: str, csv_name: str):
        """
        Create an empty CSV file with the appropriate structure.
        
        Args:
            csv_path: The path to the CSV file
            csv_name: The name of the CSV file (brand_info, best_practices, or compliance_info)
        """
        if csv_name == "brand_info":
            headers = ["Area", "Key Info"]
            data = [
                ["Brand Name", ""],
                ["Website Link", ""],
                ["Long Description", ""],
                ["Short Description", ""],
                ["Target Audience", ""],
                ["Tone of Voice", ""]
            ]
        elif csv_name == "best_practices":
            headers = ["", ""]
            data = [
                ["tipocontenuto", ""],
                ["struttura", ""],
                ["lunghezzaideale", ""],
                ["elementinecessari", ""],
                ["tonoconsigliato", ""]
            ]
        elif csv_name == "compliance_info":
            headers = ["", ""]
            data = [
                ["settore", ""],
                ["regolamentazione", ""],
                ["disclaimer_necessari", ""]
            ]
        
        with open(csv_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(data)
        
        logger.log_info(f"Created empty {csv_name} CSV file at {csv_path}")
    
    def load_brand_info(self) -> Dict[str, str]:
        """
        Load and parse the brand_info CSV file.
        
        Returns:
            A dictionary containing the brand information
        """
        logger.log_data_access("CSVManager", self.rag1_path, "read", "Loading brand info")
        try:
            df = pd.read_csv(self.rag1_path)
            # Convert the DataFrame to a dictionary
            brand_info = {}
            for _, row in df.iterrows():
                if len(row) >= 2:  # Ensure there are at least two columns
                    key = row[0]
                    value = row[1]
                    if pd.notna(key) and pd.notna(value):  # Skip NaN values
                        brand_info[key] = value
            
            logger.log_info(f"Successfully loaded brand info with {len(brand_info)} entries")
            return brand_info
        except Exception as e:
            logger.log_error(f"Error loading brand info: {str(e)}")
            return {}
    
    def load_best_practices(self) -> Dict[str, str]:
        """
        Load and parse the best_practices CSV file.
        
        Returns:
            A dictionary containing the best practices
        """
        logger.log_data_access("CSVManager", self.rag2_path, "read", "Loading best practices")
        try:
            df = pd.read_csv(self.rag2_path)
            # Convert the DataFrame to a dictionary
            best_practices = {}
            for _, row in df.iterrows():
                if len(row) >= 2:  # Ensure there are at least two columns
                    key = row[0]
                    value = row[1]
                    if pd.notna(key) and pd.notna(value):  # Skip NaN values
                        best_practices[key] = value
            
            logger.log_info(f"Successfully loaded best practices with {len(best_practices)} entries")
            return best_practices
        except Exception as e:
            logger.log_error(f"Error loading best practices: {str(e)}")
            return {}
    
    def load_compliance_info(self) -> Dict[str, str]:
        """
        Load and parse the compliance_info CSV file.
        
        Returns:
            A dictionary containing the compliance information
        """
        logger.log_data_access("CSVManager", self.rag3_path, "read", "Loading compliance info")
        try:
            df = pd.read_csv(self.rag3_path)
            # Convert the DataFrame to a dictionary
            compliance_info = {}
            for _, row in df.iterrows():
                if len(row) >= 2:  # Ensure there are at least two columns
                    key = row[0]
                    value = row[1]
                    if pd.notna(key) and pd.notna(value):  # Skip NaN values
                        compliance_info[key] = value
            
            logger.log_info(f"Successfully loaded compliance info with {len(compliance_info)} entries")
            return compliance_info
        except Exception as e:
            logger.log_error(f"Error loading compliance info: {str(e)}")
            return {}
    
    def load_all_rag_data(self) -> Dict[str, Dict[str, str]]:
        """
        Load all RAG data from the three CSV files.
        
        Returns:
            A dictionary containing all RAG data
        """
        return {
            "brand_info": self.load_brand_info(),
            "best_practices": self.load_best_practices(),
            "compliance_info": self.load_compliance_info()
        }
    
    def validate_brand_info(self, data):
        required_columns = ['brand_name', 'tone_of_voice']
        for col in required_columns:
            if col not in data.columns:
                self.logger.log_warning(f"Missing recommended column: {col} in brand_info.csv")
        return data.fillna('').to_dict()
    
    def validate_best_practices(self, data):
        if 'guideline' not in data.columns:
            self.logger.log_error("Critical column 'guideline' missing in best_practices.csv")
            return {}
        return data.fillna('').to_dict()
    
    def validate_compliance_info(self, data):
        from fuzzywuzzy import fuzz
        mandatory_rules = ['disclaimer', 'data_protection']
        found_rules = {}
        
        for rule in mandatory_rules:
            best_match = None
            best_score = 0
            for col in data.columns:
                score = fuzz.partial_ratio(rule, col.lower())
                if score > 75:
                    best_match = col
                    best_score = score
                    break
            if best_match:
                found_rules[rule] = data[best_match].iloc[0]
            else:
                self.logger.log_warning(f"No close match found for mandatory rule: {rule}")
                found_rules[rule] = 'Default placeholder - consult legal team'
        
        return found_rules