#!/usr/bin/env python3
"""
Example configuration file for LLM-Based Cybercrime Case Classification
Copy this file to config.py and modify the values as needed.
"""

# API Configuration
ANTHROPIC_API_KEY = "your_api_key_here"  # Get from https://console.anthropic.com/

# Processing Configuration
BATCH_SIZE = 5  # Number of cases to process in each batch
DELAY_BETWEEN_BATCHES = 2  # Seconds to wait between API calls to avoid rate limiting

# File Paths
INPUT_CSV = "cyber_crime_cases.csv"  # Your input dataset
SCHEMA_FILE = "schema.json"  # Classification taxonomy

# Output Configuration
OUTPUT_DIR = "output"  # Directory for output files
LOG_LEVEL = "INFO"  # Logging level: DEBUG, INFO, WARNING, ERROR

# Classification Parameters
CONFIDENCE_THRESHOLD = 0.7  # Minimum confidence score for automatic acceptance
MAX_RETRIES = 3  # Maximum number of retries for failed API calls

# Schema Update Configuration
AUTO_UPDATE_SCHEMA = True  # Automatically update schema with new tags
BACKUP_SCHEMA = True  # Create backup before schema updates
