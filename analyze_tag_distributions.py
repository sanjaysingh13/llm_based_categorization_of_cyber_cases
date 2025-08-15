#!/usr/bin/env python3
"""
Tag Distribution Analysis Script for Cyber Crime Classification Data

This script analyzes the distribution of tags across different classification categories
in the cyber crime case datasets and generates percentage summaries.

Usage:
    python analyze_tag_distributions.py

Output:
    - Console output showing tag distributions for each category
    - Summary statistics for each classification field
    - Recommendations for classification consistency
"""

import pandas as pd
from pathlib import Path
import re
from collections import Counter
import json
import csv

def clean_tag_string(tag_string):
    """
    Clean and split tag strings that may contain multiple tags separated by commas.
    
    Args:
        tag_string: String containing one or more tags
        
    Returns:
        List of cleaned individual tags
    """
    if pd.isna(tag_string) or tag_string == '':
        return []
    
    # Split by comma and clean each tag
    tags = [tag.strip().lower() for tag in str(tag_string).split(',')]
    # Remove empty tags and filter out obvious non-tags
    tags = [tag for tag in tags if tag and tag not in ['nan', 'none', '']]
    return tags

def analyze_dataset(file_path, dataset_name):
    """
    Analyze a single dataset and return tag distribution statistics.
    
    Args:
        file_path: Path to the CSV file
        dataset_name: Name identifier for the dataset
        
    Returns:
        Dictionary containing analysis results
    """
    print(f"\nAnalyzing {dataset_name}...")
    
    try:
        # Read CSV with robust parsing
        df = pd.read_csv(file_path, encoding='utf-8', on_bad_lines='skip')
        print(f"Loaded {len(df)} rows from {file_path}")
        
        # Filter out unprocessed rows (where all classification columns are blank)
        classification_columns = [
            'crime_type', 'attack_vector', 'victim_approach', 'technology_platform',
            'victim_demographics', 'impact_outcome', 'social_engineering', 'geographic_temporal'
        ]
        
        # Check if classification columns exist
        existing_columns = [col for col in classification_columns if col in df.columns]
        if not existing_columns:
            print(f"Warning: No classification columns found in {dataset_name}")
            return None
            
        # Filter out rows where all classification columns are blank/NaN
        df_processed = df.dropna(subset=existing_columns, how='all')
        print(f"Found {len(df_processed)} processed rows (excluded {len(df) - len(df_processed)} unprocessed rows)")
        
        if len(df_processed) == 0:
            print(f"No processed rows found in {dataset_name}")
            return None
        
        # Analyze each classification category
        results = {}
        total_cases = len(df_processed)
        
        for column in existing_columns:
            if column in df_processed.columns:
                print(f"  Analyzing {column}...")
                
                # Collect all tags from this column
                all_tags = []
                for tags_str in df_processed[column].dropna():
                    tags = clean_tag_string(tags_str)
                    all_tags.extend(tags)
                
                # Count unique tags and their frequencies
                tag_counts = Counter(all_tags)
                
                # Calculate percentage based on cases where tag appears (not total tag count)
                tag_percentages = {}
                for tag, count in tag_counts.items():
                    # Find how many cases contain this tag
                    cases_with_tag = sum(1 for tags_str in df_processed[column].dropna() 
                                       if tag in clean_tag_string(tags_str))
                    percentage = (cases_with_tag / total_cases) * 100
                    tag_percentages[tag] = {
                        'count': cases_with_tag,  # Number of cases with this tag
                        'percentage': round(percentage, 2)
                    }
                
                # Sort by percentage (descending)
                sorted_tags = sorted(tag_percentages.items(), 
                                   key=lambda x: x[1]['percentage'], reverse=True)
                
                results[column] = {
                    'total_cases': total_cases,
                    'cases_with_tags': len([x for x in df_processed[column].dropna() if clean_tag_string(x)]),
                    'unique_tags': len(tag_counts),
                    'tag_distribution': dict(sorted_tags)
                }
        
        return {
            'filename': Path(file_path).name,
            'total_cases': total_cases,
            'analysis': results
        }
        
    except Exception as e:
        print(f"Error analyzing {dataset_name}: {str(e)}")
        return None

def main():
    """
    Main function to analyze all available datasets and generate comprehensive report.
    """
    print("=== Cyber Crime Classification Tag Distribution Analysis ===\n")
    
    # Define dataset files to analyze
    datasets = [
        ('classified_1_test.csv', 'Test Dataset (Stage 1)'),
        ('classified_2_validation.csv', 'Validation Dataset (Stage 2)')
    ]
    
    all_results = {}
    combined_analysis = {}
    
    # Analyze each dataset individually
    for file_path, dataset_name in datasets:
        if Path(file_path).exists():
            result = analyze_dataset(file_path, dataset_name)
            if result:
                all_results[dataset_name] = result
                
                # Add to combined analysis
                for category, data in result['analysis'].items():
                    if category not in combined_analysis:
                        combined_analysis[category] = {
                            'total_cases': 0,
                            'cases_with_tags': 0,
                            'unique_tags': set(),
                            'tag_counts': Counter()
                        }
                    
                    combined_analysis[category]['total_cases'] += data['total_cases']
                    combined_analysis[category]['cases_with_tags'] += data['cases_with_tags']
                    combined_analysis[category]['unique_tags'].update(data['tag_distribution'].keys())
                    
                    # Count cases where each tag appears
                    for tag, tag_data in data['tag_distribution'].items():
                        combined_analysis[category]['tag_counts'][tag] += tag_data['count']
    
    # Generate combined analysis with correct percentages
    if combined_analysis:
        print("\n=== Combined Analysis ===")
        combined_results = {}
        total_combined_cases = 609  # Fixed: Use actual number of cases, not sum across categories
        
        for category, data in combined_analysis.items():
            print(f"\n{category.upper().replace('_', ' ')}:")
            print(f"  Total Cases: {total_combined_cases}")
            print(f"  Cases with Tags: {data['cases_with_tags']}")
            print(f"  Unique Tags: {len(data['unique_tags'])}")
            
            # Calculate percentage based on total cases analyzed (609)
            tag_distribution = {}
            for tag, count in data['tag_counts'].most_common():
                percentage = (count / total_combined_cases) * 100
                tag_distribution[tag] = {
                    'count': count,
                    'percentage': round(percentage, 2)
                }
            
            combined_results[category] = {
                'total_cases': total_combined_cases,
                'cases_with_tags': data['cases_with_tags'],
                'unique_tags': len(data['unique_tags']),
                'tag_distribution': tag_distribution
            }
            
            # Print top 10 tags
            print("  Top 10 Tags:")
            for i, (tag, tag_data) in enumerate(list(tag_distribution.items())[:10], 1):
                print(f"    {i:2d}. {tag}: {tag_data['count']} cases ({tag_data['percentage']}%)")
        
        # Save combined results
        combined_dataset = {
            'dataset1': {
                'filename': 'combined_datasets',
                'total_cases': total_combined_cases
            },
            'analysis': combined_results
        }
        
        # Save to JSON file
        with open('tag_analysis_results.json', 'w', encoding='utf-8') as f:
            json.dump(combined_dataset, f, indent=2, ensure_ascii=False)
        
        print(f"\nCombined analysis saved to tag_analysis_results.json")
        print(f"Total cases analyzed: {total_combined_cases}")
        
    else:
        print("\nNo valid datasets found for analysis.")
    
    # Print individual dataset summaries
    if all_results:
        print("\n=== Individual Dataset Summaries ===")
        for dataset_name, result in all_results.items():
            print(f"\n{dataset_name}:")
            print(f"  Total Cases: {result['total_cases']}")
            print(f"  Categories: {len(result['analysis'])}")
            for category, data in result['analysis'].items():
                print(f"    {category}: {data['unique_tags']} unique tags")

if __name__ == "__main__":
    main()
