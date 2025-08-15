#!/usr/bin/env python3
"""
Schema Update Script for Cybercrime Classification

This script analyzes a classification results CSV file and automatically
adds any new tags that don't exist in the current schema.json file.

Usage:
    python update_schema_from_results.py                           # Uses classified_1_test.csv by default
    python update_schema_from_results.py classified_2_validation.csv  # Analyze specific file
    python update_schema_from_results.py classified_3_final.csv      # Analyze final results

The script will:
1. Load the current schema.json
2. Extract unique tags from each classification column in the specified CSV
3. Add missing tags to the appropriate categories in schema.json
4. Save the updated schema.json
5. Provide a summary of changes made
"""

import pandas as pd
import json
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SchemaUpdater:
    def __init__(self, results_file: str = "classified_1_test.csv"):
        """Initialize the schema updater with file paths"""
        self.schema_file = Path("schema.json")
        self.results_file = Path(results_file)
        self.backup_file = Path("schema_backup.json")
        
        # Validate that required files exist
        if not self.schema_file.exists():
            raise FileNotFoundError(f"Schema file not found: {self.schema_file}")
        if not self.results_file.exists():
            raise FileNotFoundError(f"Results file not found: {self.results_file}")
        
        logger.info(f"Will analyze results from: {self.results_file}")
    
    def load_schema(self) -> Dict:
        """Load the current schema from JSON file"""
        try:
            with open(self.schema_file, 'r', encoding='utf-8') as f:
                schema = json.load(f)
            logger.info(f"Loaded schema from {self.schema_file}")
            return schema
        except Exception as e:
            logger.error(f"Failed to load schema: {e}")
            raise
    
    def load_results(self) -> pd.DataFrame:
        """Load the classification results from CSV file"""
        try:
            df = pd.read_csv(self.results_file)
            logger.info(f"Loaded results from {self.results_file}: {len(df)} cases")
            return df
        except Exception as e:
            logger.error(f"Failed to load results: {e}")
            raise
    
    def extract_tags_from_column(self, df: pd.DataFrame, column_name: str) -> Set[str]:
        """
        Extract all unique tags from a specific column
        
        Args:
            df: DataFrame with classification results
            column_name: Name of the column to extract tags from
            
        Returns:
            Set of unique tags found in the column
        """
        if column_name not in df.columns:
            return set()
        
        all_tags = set()
        for value in df[column_name]:
            if pd.isna(value) or value == '':
                continue
            
            # Split by comma and clean each tag
            tags = [tag.strip() for tag in str(value).split(',')]
            all_tags.update(tags)
        
        # Remove empty strings and normalize
        all_tags = {tag for tag in all_tags if tag and tag.lower() not in ['nan', 'none']}
        return all_tags
    
    def get_existing_tags_from_schema(self, schema: Dict) -> Dict[str, Set[str]]:
        """
        Get all existing tags from the current schema
        
        Args:
            schema: The loaded schema dictionary
            
        Returns:
            Dictionary mapping category names to sets of existing tags
        """
        existing_tags = {}
        
        # Handle the nested schema structure
        if "schema" in schema:
            schema_content = schema["schema"]
        else:
            schema_content = schema
        
        for main_category, subcategories in schema_content.items():
            category_tags = set()
            for subcategory_name, tag_list in subcategories.items():
                if isinstance(tag_list, list):
                    category_tags.update(tag_list)
                elif isinstance(tag_list, str):
                    category_tags.add(tag_list)
            existing_tags[main_category] = category_tags
        
        return existing_tags
    
    def find_new_tags(self, df: pd.DataFrame, existing_tags: Dict[str, Set[str]]) -> Dict[str, Set[str]]:
        """
        Find new tags in the results that don't exist in the current schema
        
        Args:
            df: DataFrame with classification results
            existing_tags: Dictionary of existing tags by category
            
        Returns:
            Dictionary mapping category names to sets of new tags
        """
        new_tags = {}
        
        # Define the classification columns to analyze
        classification_columns = [
            'crime_type', 'attack_vector', 'victim_approach', 
            'technology_platform', 'victim_demographics', 
            'impact_outcome', 'social_engineering', 'geographic_temporal'
        ]
        
        for column in classification_columns:
            if column not in df.columns:
                logger.warning(f"Column {column} not found in results file")
                continue
            
            # Extract all tags from this column
            all_tags_in_column = self.extract_tags_from_column(df, column)
            
            # Find tags that don't exist in the current schema
            existing_in_category = existing_tags.get(column, set())
            new_in_category = all_tags_in_column - existing_in_category
            
            if new_in_category:
                new_tags[column] = new_in_category
                logger.info(f"Found {len(new_in_category)} new tags in {column}: {new_in_category}")
        
        return new_tags
    
    def add_new_tags_to_schema(self, schema: Dict, new_tags: Dict[str, Set[str]]) -> Tuple[Dict, Dict[str, List[str]]]:
        """
        Add new tags to the appropriate categories in the schema
        
        Args:
            schema: The current schema dictionary
            new_tags: Dictionary of new tags by category
            
        Returns:
            Tuple of (updated_schema, changes_made)
        """
        # Create a backup before making changes
        self.create_backup(schema)
        
        # Handle the nested schema structure
        if "schema" in schema:
            schema_content = schema["schema"]
        else:
            schema_content = schema
        
        changes_made = {}
        
        for category, tags_to_add in new_tags.items():
            if category not in schema_content:
                logger.warning(f"Category {category} not found in schema, creating it")
                schema_content[category] = {}
            
            # Add new tags to an "other" subcategory for simplicity
            if "other" not in schema_content[category]:
                schema_content[category]["other"] = []
            
            for tag in tags_to_add:
                if tag not in schema_content[category]["other"]:
                    schema_content[category]["other"].append(tag)
                    logger.info(f"Added '{tag}' to 'other' subcategory in '{category}'")
                    
                    # Track changes
                    if category not in changes_made:
                        changes_made[category] = []
                    changes_made[category].append(tag)
        
        return schema, changes_made
    
    def create_backup(self, schema: Dict):
        """Create a backup of the current schema before making changes"""
        try:
            with open(self.backup_file, 'w', encoding='utf-8') as f:
                json.dump(schema, f, indent=2, ensure_ascii=False)
            logger.info(f"Schema backup created: {self.backup_file}")
        except Exception as e:
            logger.warning(f"Failed to create backup: {e}")
    
    def save_updated_schema(self, schema: Dict):
        """Save the updated schema back to the file"""
        try:
            with open(self.schema_file, 'w', encoding='utf-8') as f:
                json.dump(schema, f, indent=2, ensure_ascii=False)
            logger.info(f"Updated schema saved to {self.schema_file}")
        except Exception as e:
            logger.error(f"Failed to save updated schema: {e}")
            raise
    
    def run_update(self) -> Dict[str, List[str]]:
        """
        Main method to run the complete schema update process
        
        Returns:
            Dictionary of changes made by category
        """
        logger.info("Starting schema update process...")
        
        try:
            # Load current schema and results
            schema = self.load_schema()
            results_df = self.load_results()
            
            # Get existing tags from schema
            existing_tags = self.get_existing_tags_from_schema(schema)
            logger.info(f"Found {sum(len(tags) for tags in existing_tags.values())} existing tags across {len(existing_tags)} categories")
            
            # Find new tags in results
            new_tags = self.find_new_tags(results_df, existing_tags)
            
            if not new_tags:
                logger.info("No new tags found. Schema is up to date.")
                return {}
            
            # Add new tags to schema
            updated_schema, changes_made = self.add_new_tags_to_schema(schema, new_tags)
            
            # Save updated schema
            self.save_updated_schema(updated_schema)
            
            # Print summary
            self.print_summary(changes_made)
            
            return changes_made
            
        except Exception as e:
            logger.error(f"Schema update failed: {e}")
            raise
    
    def print_summary(self, changes_made: Dict[str, List[str]]):
        """Print a summary of all changes made"""
        print("\n" + "="*60)
        print("SCHEMA UPDATE SUMMARY")
        print("="*60)
        
        if not changes_made:
            print("✅ No new tags found. Schema is up to date.")
            return
        
        total_new_tags = sum(len(tags) for tags in changes_made.values())
        print(f"✅ Added {total_new_tags} new tags to the schema:")
        
        for category, tags in changes_made.items():
            print(f"\n📁 {category.upper()}:")
            for tag in sorted(tags):
                print(f"   ➕ {tag}")
        
        print(f"\n📁 Schema file updated: {self.schema_file}")
        print(f"📁 Backup created: {self.backup_file}")
        print(f"\n💡 You can now continue with the main workflow!")
        print("="*60)

def main():
    """Main function to run the schema updater"""
    try:
        # Get the CSV file to analyze from command line argument, or use default
        if len(sys.argv) > 1:
            csv_file = sys.argv[1]
        else:
            csv_file = "classified_1_test.csv"
        
        print(f"🔍 Analyzing results from: {csv_file}")
        
        updater = SchemaUpdater(csv_file)
        changes = updater.run_update()
        
        if changes:
            print(f"\n🎉 Schema update completed successfully!")
            print(f"Added {sum(len(tags) for tags in changes.values())} new tags.")
        else:
            print("\n✨ Schema is already up to date!")
            
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        print("Please ensure both 'schema.json' and the specified CSV file exist in the current directory.")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print("Check the logs above for more details.")

if __name__ == "__main__":
    main()
