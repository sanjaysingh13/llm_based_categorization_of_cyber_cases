#!/usr/bin/env python3
"""
Demo script for LLM-Based Cybercrime Case Classification
This script demonstrates the basic workflow with a small sample of data.
"""

import os
import pandas as pd
from pathlib import Path
from semi_automated_classification import SemiAutomatedCybercrimeClassifier
import json

def create_demo_dataset():
    """Create a small demo dataset for testing"""
    demo_data = [
        {
            "Case": "DEMO_001",
            "Gist": "Victim received WhatsApp message from unknown number claiming to be bank official, asking for OTP to resolve account issue. Victim shared OTP and lost Rs. 50,000 from bank account."
        },
        {
            "Case": "DEMO_002", 
            "Gist": "Victim saw fake investment opportunity on Facebook ad promising 200% returns in 30 days. Invested Rs. 25,000 but never received returns or could contact the company."
        },
        {
            "Case": "DEMO_003",
            "Gist": "Victim received call from person claiming to be from IT department saying victim's Aadhaar was linked to criminal activities. Victim transferred Rs. 75,000 to 'resolve' the issue."
        }
    ]
    
    df = pd.DataFrame(demo_data)
    df.to_csv("demo_cases.csv", index=False)
    print("✅ Created demo_cases.csv with 3 sample cases")
    return "demo_cases.csv"

def run_demo():
    """Run a demonstration of the classification system"""
    print("🚀 LLM-Based Cybercrime Case Classification - Demo")
    print("=" * 60)
    
    # Check if API key is set
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key or api_key == "your_api_key_here":
        print("❌ Please set your Anthropic API key in .env file")
        print("   Get your key from: https://console.anthropic.com/")
        return
    
    # Create demo dataset
    demo_file = create_demo_dataset()
    
    # Initialize classifier
    print("\n🔧 Initializing classifier...")
    classifier = SemiAutomatedCybercrimeClassifier(api_key)
    
    # Load schema
    if not Path("schema.json").exists():
        print("❌ schema.json not found. Please ensure it exists in the project directory.")
        return
    
    with open("schema.json", "r") as f:
        schema = json.load(f)
    
    print("✅ Schema loaded successfully")
    
    # Process demo cases
    print(f"\n📊 Processing {len(pd.read_csv(demo_file))} demo cases...")
    print("   This will take a few minutes and cost approximately $0.05-0.10")
    
    try:
        # Process demo cases
        results = classifier.process_cases(
            csv_file=demo_file,
            schema=schema,
            output_file="demo_results.csv"
        )
        
        print("\n✅ Demo completed successfully!")
        print(f"   Results saved to: demo_results.csv")
        print(f"   Total cases processed: {len(results)}")
        
        # Show sample results
        print("\n📋 Sample Results:")
        df = pd.read_csv("demo_results.csv")
        for _, row in df.iterrows():
            print(f"   Case {row['Case']}: {row.get('crime_type', 'N/A')}")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        print("   Check your API key and internet connection")

if __name__ == "__main__":
    run_demo()
