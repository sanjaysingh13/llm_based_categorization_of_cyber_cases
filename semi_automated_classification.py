import pandas as pd
import json
import asyncio
import aiohttp
import time
from typing import Dict, List, Optional, Set
import logging
from pathlib import Path
import random
import os

class SemiAutomatedCybercrimeClassifier:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.anthropic.com/v1/messages"
        self.headers = {
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        
        # Validate API key format
        if not api_key.startswith('sk-'):
            raise ValueError("Invalid API key format. Anthropic API keys should start with 'sk-'")
        
        # Setup logging with more detail
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)

    def create_schema_discovery_prompt(self, cases_sample: List[Dict]) -> str:
        """Create prompt for initial schema discovery from sample cases"""
        cases_text = "\n\n".join([
            f"CASE {i+1}:\nCase ID: {case['Case']}\nDescription: {case['Gist']}"
            for i, case in enumerate(cases_sample[:10])  # Show first 10 for context
        ])
        
        prompt = f"""
You are analyzing cybercrime cases to create a classification taxonomy. Here are sample cases:

{cases_text}

Based on these cases and your knowledge of cybercrime patterns, create a comprehensive classification schema with these exact keys:

1. "primary_categories": Main types of cybercrimes
2. "attack_methods": Technical/procedural methods used by criminals  
3. "victim_targeting": How victims are identified and approached
4. "communication_channels": Platforms/methods used for communication
5. "payment_methods": How money/value is extracted from victims
6. "impersonation_types": What entities criminals pretend to be

For each key, provide a list of relevant values that could apply across different cases. Make the values:
- Specific enough to be useful for analysis
- General enough to apply to multiple cases
- Use snake_case formatting (e.g., "fake_investment_platform")

Return ONLY a valid JSON object with the schema. No additional text.

Example structure:
{{
    "primary_categories": ["investment_fraud", "romance_scam", ...],
    "attack_methods": ["fake_website", "phishing_email", ...],
    ...
}}
        """
        return prompt

    def create_classification_prompt(self, gist: str, case_id: str, schema: Dict) -> str:
        """Create prompt for classifying a case using provided schema"""
        # Handle nested schema structure
        if "schema" in schema:
            schema = schema["schema"]
        
        # Flatten the schema to show all available values
        flattened_values = {}
        for main_category, subcategories in schema.items():
            all_values = []
            for subcat_name, values in subcategories.items():
                all_values.extend(values)
            flattened_values[main_category] = all_values
        
        schema_str = json.dumps(schema, indent=2)
        flattened_str = json.dumps(flattened_values, indent=2)
        
        prompt = f"""
Analyze this cybercrime case and classify it using the provided hierarchical schema.

CASE ID: {case_id}
CASE DESCRIPTION: {gist}

FULL HIERARCHICAL SCHEMA:
{schema_str}

FLATTENED VALUES FOR REFERENCE:
{flattened_str}

The schema has main categories, each with subcategories containing specific values. 
You should select specific values from the lists, not the subcategory names.

For example:
- For victim_approach, choose from: "cold_call", "whatsapp_message", "social_media_friend_request", "dating_app_match", etc.
- For crime_type, choose from: "task_based_fraud", "investment_scam", "child_exploitation", "sim_card_fraud", etc.

Classify this case using the following JSON format:

{{
    "case_id": "{case_id}",
    "crime_type": ["specific values from crime_type subcategory lists"],
    "attack_vector": ["specific values from attack_vector subcategory lists"],
    "victim_approach": ["specific values from victim_approach subcategory lists"],
    "technology_platform": ["specific values from technology_platform subcategory lists"],
    "victim_demographics": ["specific values from victim_demographics subcategory lists"],
    "impact_outcome": ["specific values from impact_outcome subcategory lists"],
    "social_engineering": ["specific values from social_engineering subcategory lists"],
    "geographic_temporal": ["specific values from geographic_temporal subcategory lists"],
    "confidence_score": 0.85,
    "notes": "any additional observations about this case"
}}

CLASSIFICATION RULES:
1. Use ONLY the specific values from within the subcategory lists, NOT the subcategory names
2. For each main category, select ALL applicable specific values
3. Each field can have 0 or more applicable values as a list
4. If no specific values fit for a main category, use empty list []
5. Be comprehensive - a case can have multiple applicable values per category
6. confidence_score should be 0.0-1.0 based on case clarity
7. Add notes about reasoning, unique aspects, or uncertainty

I will add some gotchas because you might not be aware of the context specific to Indian cybercrime.

8. If a person has been put under fear by perpretator, pretending to be a government official, by mentioning that his identity has been used for a crime, or that a parcel in his name has contraband, add ;'digital_arrest' to the classification, even if the words are not specifically mentioned.

9. You sometimes misclassify a case where a victim falls for a Facebook Ad from the perpretrators and you misclassiy it as 'social_media_friend_request' whereas it should be 'facebook_ad'.
Similarly, look out for other fake ad methods for reaching out to victim. 

10. The tag 'fraud_by_impersonation_of_influential_person' will only apply if the impersonation is of a prominent person whom the victim is likely to know, such as a department superior, a minister or a public figure. 

11. You sometimes misclassify a case where a known person has misused subsidy as a 'subsidy_fraud'. The tag is only applicable when an unknown perpetrator has used subsidy as a bait. No subsidy tranfer would have actually taken place in that case. Your 'subsidy_fraud' classification may actually be 'not_a_cyber_crime' as it pertains to misappropriation of subsidy already granted.

12. 'corporate_impersonation' should not generally be aplied to impersonation of bank representatives, as almost all cyber-crime cases would have this feature. The tag should only refer to impersonation of a well-known company.

13. 'qr_code_for_debiting_fraudulently_presented_as_crediting' is a tag where the victim thinks that he or she is scanning a code to receive money, whereas it is actually a code for sending money to the fraudster.

14. 'traditional_cheating_and_fraud' will generally apply where there is some prior acquaintainance between victim and perpretrator in the real world. It will also be indicated if the perpetrator has some in-depth knowledge about the victim, like he is constructing a house and the scam involves cement delivery. Or it is related to the victim's trade or business. Cyber criminals generally operate in an anonymous and non-discriminating environment.

15. 'CSP_fraud' is a local type of cybercrime of which you might not be aware. Customer Sevice Point (CSP) is a grass-root level customer service provider for banks. Generally shthe fraud will be for fake CSP installation.

16. "AEPS_fraud' is a similar local type of cybercrime involving Aadhar Enabled Payment System. Money can be withdrawn from the victim's account by using the victim's Aadhar number and biometrics, by obtaining the biometric data of the victim illegally.

17. 'suo_moto_case' will refer to cases initiated by police officers themselves, after developing information, such as information about fake call centres or a special ant-cybercrime drive based on intelligence and analysis.

18. 'general_purpose_fir_suitable_for_wider_investigation' will refer to cases where the complaint goes beyond a specific crime instance and will enable investigations into the wider gamut of that category of cybercrime, including the enabler ecosystems.

Examples of CORRECT selections:
- crime_type: ["investment_scam", "job_fraud"] (specific values, not "financial_fraud")
- victim_approach: ["whatsapp_message", "social_media_friend_request"] (specific values, not "direct_contact" or "platform_based")
- technology_platform: ["whatsapp", "facebook", "upi_apps"] (specific platforms used)

Return only the JSON response.
        """
        return prompt

    async def discover_schema(self, cases_sample: List[Dict]) -> Dict:
        """Use LLM to discover initial schema from sample cases"""
        prompt = self.create_schema_discovery_prompt(cases_sample)
        
        payload = {
            "model": "claude-3-5-sonnet-20241022",  # Updated to latest model
            "max_tokens": 2000,
            "temperature": 0.3,
            "messages": [{"role": "user", "content": prompt}]
        }
        
        connector = aiohttp.TCPConnector(limit=1)
        timeout = aiohttp.ClientTimeout(total=60)
        
        async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
            async with session.post(self.base_url, headers=self.headers, json=payload) as response:
                if response.status == 200:
                    result = await response.json()
                    content = result['content'][0]['text']
                    try:
                        schema = json.loads(content)
                        return schema
                    except json.JSONDecodeError as e:
                        self.logger.error(f"Failed to parse schema JSON: {e}")
                        return self.get_fallback_schema()
                elif response.status == 401:
                    self.logger.error("Authentication failed in schema discovery. Please check your API key.")
                    return self.get_fallback_schema()
                else:
                    error_text = await response.text()
                    self.logger.error(f"API error in schema discovery: {response.status} - {error_text}")
                    return self.get_fallback_schema()

    def get_all_schema_values(self, schema: Dict) -> Dict:
        """Extract all specific values from the hierarchical schema"""
        if "schema" in schema:
            schema = schema["schema"]
        
        all_values = {}
        for main_category, subcategories in schema.items():
            category_values = []
            for subcat_name, values in subcategories.items():
                category_values.extend(values)
            all_values[main_category] = category_values
        
        return all_values
    def get_fallback_schema(self) -> Dict:
        """Fallback schema if API call fails - simplified version"""
        return {
            "crime_type": {
                "financial_fraud": ["investment_scam", "job_fraud", "loan_fraud"],
                "identity_crimes": ["sim_card_fraud", "account_takeover"]
            },
            "attack_vector": {
                "technical": ["phishing_link", "malicious_app"],
                "social": ["impersonation", "relationship_building"]
            },
            "victim_approach": {
                "direct_contact": ["cold_call", "whatsapp_message"],
                "platform_based": ["social_media_friend_request", "dating_app_match"]
            },
            "technology_platform": {
                "messaging": ["whatsapp", "telegram"],
                "social_media": ["facebook", "instagram"]
            },
            "victim_demographics": {
                "age_group": ["young_adult", "elderly"],
                "tech_familiarity": ["novice", "advanced"]
            },
            "impact_outcome": {
                "financial": ["direct_monetary_loss"],
                "personal": ["privacy_breach", "emotional_trauma"]
            },
            "social_engineering": {
                "pressure_tactics": ["time_pressure", "authority_pressure"]
            },
            "geographic_temporal": {
                "location": ["local", "cross_border"]
            }
        }

    async def classify_single_case(self, session: aiohttp.ClientSession, case_id: str, gist: str, schema: Dict) -> Dict:
        """Classify a single case using the provided schema"""
        prompt = self.create_classification_prompt(gist, case_id, schema)
        
        payload = {
            "model": "claude-3-5-sonnet-20241022",  # Updated to latest model
            "max_tokens": 1000,
            "temperature": 0.1,
            "messages": [{"role": "user", "content": prompt}]
        }
        
        try:
            async with session.post(self.base_url, headers=self.headers, json=payload) as response:
                if response.status == 200:
                    result = await response.json()
                    content = result['content'][0]['text']
                    try:
                        classification = json.loads(content)
                        # Add success status
                        classification['status'] = 'success'
                        return classification
                    except json.JSONDecodeError as e:
                        self.logger.error(f"JSON decode error for case {case_id}: {str(e)}")
                        return self.create_error_response(case_id, f"JSON decode error: {str(e)}")
                elif response.status == 401:
                    error_msg = "API key invalid or missing. Please check your ANTHROPIC_API_KEY environment variable."
                    self.logger.error(f"Authentication failed for case {case_id}: {error_msg}")
                    return self.create_error_response(case_id, f"Authentication failed: {error_msg}")
                elif response.status == 429:
                    error_msg = "Rate limit exceeded. Please wait before retrying."
                    self.logger.warning(f"Rate limit hit for case {case_id}: {error_msg}")
                    return self.create_error_response(case_id, f"Rate limit: {error_msg}")
                else:
                    error_text = await response.text()
                    error_msg = f"API error {response.status}: {error_text}"
                    self.logger.error(f"API error for case {case_id}: {error_msg}")
                    return self.create_error_response(case_id, error_msg)
        except aiohttp.ClientError as e:
            error_msg = f"Network error: {str(e)}"
            self.logger.error(f"Network error for case {case_id}: {error_msg}")
            return self.create_error_response(case_id, error_msg)
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            self.logger.error(f"Unexpected error for case {case_id}: {error_msg}")
            return self.create_error_response(case_id, error_msg)

    def create_error_response(self, case_id: str, error: str) -> Dict:
        """Create error response with schema keys"""
        return {
            'case_id': case_id,
            'crime_type': [],
            'attack_vector': [],
            'victim_approach': [],
            'technology_platform': [],
            'victim_demographics': [],
            'impact_outcome': [],
            'social_engineering': [],
            'geographic_temporal': [],
            'confidence_score': 0.0,
            'notes': f'Error: {error}'
        }

    def serialize_list_field(self, field) -> str:
        """Safely serialize list fields to comma-separated strings"""
        if isinstance(field, list):
            return ', '.join(str(item) for item in field)
        return str(field) if field else ''

    async def process_iteration(self, df: pd.DataFrame, sample_size: int, 
                               excluded_cases: Set[str], schema: Optional[Dict] = None,
                               iteration_name: str = "iteration", resume_from_file: str = None) -> tuple:
        """Process one iteration of classification with resume capability"""
        
        # Check for existing progress file to resume from
        progress_file = f"progress_{iteration_name}.csv"
        checkpoint_file = f"checkpoint_{iteration_name}.json"
        
        already_processed = set()
        partial_results = []
        
        if resume_from_file and Path(resume_from_file).exists():
            self.logger.info(f"Resuming from existing file: {resume_from_file}")
            existing_df = pd.read_csv(resume_from_file)
            already_processed = set(existing_df['Case'].values)
            partial_results = existing_df.to_dict('records')
            self.logger.info(f"Found {len(already_processed)} already processed cases")
        
        # Sample cases, excluding already processed ones
        available_cases = df[~df['Case'].isin(excluded_cases.union(already_processed))]
        remaining_to_process = min(sample_size - len(already_processed), len(available_cases))
        
        if remaining_to_process <= 0:
            self.logger.info("All cases already processed!")
            output_df = pd.DataFrame(partial_results) if partial_results else df.iloc[:0].copy()
            return output_df, schema, excluded_cases.union(already_processed)
        
        sample_df = available_cases.sample(n=remaining_to_process, random_state=42)
        self.logger.info(f"Processing {len(sample_df)} new cases for {iteration_name} (resume mode)")
        
        # Discover schema if not provided (first iteration only)
        if schema is None:
            self.logger.info("Discovering schema from sample cases...")
            cases_for_schema = sample_df.to_dict('records')
            schema = await self.discover_schema(cases_for_schema)
            
            # Save discovered schema
            schema_file = f"schema_{iteration_name}.json"
            with open(schema_file, 'w') as f:
                json.dump(schema, f, indent=2)
            self.logger.info(f"Schema saved to {schema_file}")
        
        # Save checkpoint info
        checkpoint_data = {
            'iteration_name': iteration_name,
            'total_target': sample_size,
            'already_processed': len(already_processed),
            'remaining_to_process': remaining_to_process,
            'timestamp': time.time()
        }
        with open(checkpoint_file, 'w') as f:
            json.dump(checkpoint_data, f, indent=2)
        
        # Process in smaller batches with frequent saves
        connector = aiohttp.TCPConnector(limit=3)  # Reduced concurrency for stability
        timeout = aiohttp.ClientTimeout(total=120)  # Increased timeout
        
        async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
            batch_size = 5  # Smaller batch size for more frequent saves
            new_results = []
            
            for i in range(0, len(sample_df), batch_size):
                batch_df = sample_df.iloc[i:i + batch_size]
                self.logger.info(f"Processing batch {i//batch_size + 1}/{(len(sample_df)-1)//batch_size + 1}")
                
                # Process batch with better error handling
                batch_tasks = []
                for _, row in batch_df.iterrows():
                    task = self.classify_single_case(session, row['Case'], row['Gist'], schema)
                    batch_tasks.append(task)
                
                try:
                    batch_results = await asyncio.gather(*batch_tasks, return_exceptions=True)
                    
                    # Handle exceptions in batch
                    for j, result in enumerate(batch_results):
                        if isinstance(result, Exception):
                            case_id = batch_df.iloc[j]['Case']
                            self.logger.error(f"Task exception for {case_id}: {str(result)}")
                            result = self.create_error_response(case_id, f"Processing error: {str(result)}")
                        elif result.get('status') != 'success':
                            # Log failed classifications for debugging
                            self.logger.warning(f"Failed classification for {result.get('case_id', 'unknown')}: {result.get('notes', 'no details')}")
                        new_results.append(result)
                    
                    # Save progress after each batch
                    self.save_incremental_progress(df, partial_results + new_results, 
                                                 progress_file, iteration_name)
                    
                    # Log batch completion
                    successful = sum(1 for r in batch_results if isinstance(r, dict) and r.get('status') == 'success')
                    self.logger.info(f"Batch completed: {successful}/{len(batch_results)} successful")
                    
                    # Small delay between batches to avoid rate limits
                    await asyncio.sleep(2)  # Increased delay
                    
                except Exception as e:
                    self.logger.error(f"Batch processing error: {str(e)}")
                    # Save what we have so far
                    if new_results:
                        self.save_incremental_progress(df, partial_results + new_results, 
                                                     progress_file, iteration_name)
                    raise e
        
        # Combine all results
        all_results = partial_results + new_results
        
        # Convert to final DataFrame
        results_df = pd.DataFrame([r for r in all_results if 'case_id' in r])
        
        # Merge with original data
        case_ids = [r['case_id'] for r in all_results if 'case_id' in r]
        output_df = df[df['Case'].isin(case_ids)].copy()
        
        # Add classification columns with safe serialization and error handling
        for case_result in all_results:
            if 'case_id' not in case_result:
                continue
            case_mask = output_df['Case'] == case_result['case_id']
            if case_mask.any():
                try:
                    output_df.loc[case_mask, 'crime_type'] = self.serialize_list_field(case_result.get('crime_type', []))
                    output_df.loc[case_mask, 'attack_vector'] = self.serialize_list_field(case_result.get('attack_vector', []))
                    output_df.loc[case_mask, 'victim_approach'] = self.serialize_list_field(case_result.get('victim_approach', []))
                    output_df.loc[case_mask, 'technology_platform'] = self.serialize_list_field(case_result.get('technology_platform', []))
                    output_df.loc[case_mask, 'victim_demographics'] = self.serialize_list_field(case_result.get('victim_demographics', []))
                    output_df.loc[case_mask, 'impact_outcome'] = self.serialize_list_field(case_result.get('impact_outcome', []))
                    output_df.loc[case_mask, 'social_engineering'] = self.serialize_list_field(case_result.get('social_engineering', []))
                    output_df.loc[case_mask, 'geographic_temporal'] = self.serialize_list_field(case_result.get('geographic_temporal', []))
                    output_df.loc[case_mask, 'confidence_score'] = case_result.get('confidence_score', 0.0)
                    output_df.loc[case_mask, 'classification_notes'] = case_result.get('notes', '')
                except Exception as e:
                    self.logger.error(f"Error setting values for case {case_result['case_id']}: {str(e)}")
                    # Set default values on error
                    output_df.loc[case_mask, 'crime_type'] = ''
                    output_df.loc[case_mask, 'attack_vector'] = ''
                    output_df.loc[case_mask, 'victim_approach'] = ''
                    output_df.loc[case_mask, 'technology_platform'] = ''
                    output_df.loc[case_mask, 'victim_demographics'] = ''
                    output_df.loc[case_mask, 'impact_outcome'] = ''
                    output_df.loc[case_mask, 'social_engineering'] = ''
                    output_df.loc[case_mask, 'geographic_temporal'] = ''
                    output_df.loc[case_mask, 'confidence_score'] = 0.0
                    output_df.loc[case_mask, 'classification_notes'] = f'Error processing: {str(e)}'
        
        # Save final output
        output_file = f"classified_{iteration_name}.csv"
        output_df.to_csv(output_file, index=False)
        self.logger.info(f"Final results saved to {output_file}")
        
        # Clean up progress files
        for temp_file in [progress_file, checkpoint_file]:
            if Path(temp_file).exists():
                Path(temp_file).unlink()
        
        return output_df, schema, set(output_df['Case'].values)

    def save_incremental_progress(self, original_df: pd.DataFrame, results: List[Dict], 
                                progress_file: str, iteration_name: str):
        """Save incremental progress to allow resuming"""
        try:
            if not results:
                return
                
            # Get processed case IDs
            case_ids = [r['case_id'] for r in results if 'case_id' in r]
            if not case_ids:
                return
                
            # Create progress DataFrame
            progress_df = original_df[original_df['Case'].isin(case_ids)].copy()
            
            # Add classification columns
            for case_result in results:
                if 'case_id' not in case_result:
                    continue
                case_mask = progress_df['Case'] == case_result['case_id']
                if case_mask.any():
                    progress_df.loc[case_mask, 'crime_type'] = self.serialize_list_field(case_result.get('crime_type', []))
                    progress_df.loc[case_mask, 'attack_vector'] = self.serialize_list_field(case_result.get('attack_vector', []))
                    progress_df.loc[case_mask, 'victim_approach'] = self.serialize_list_field(case_result.get('victim_approach', []))
                    progress_df.loc[case_mask, 'technology_platform'] = self.serialize_list_field(case_result.get('technology_platform', []))
                    progress_df.loc[case_mask, 'victim_demographics'] = self.serialize_list_field(case_result.get('victim_demographics', []))
                    progress_df.loc[case_mask, 'impact_outcome'] = self.serialize_list_field(case_result.get('impact_outcome', []))
                    progress_df.loc[case_mask, 'social_engineering'] = self.serialize_list_field(case_result.get('social_engineering', []))
                    progress_df.loc[case_mask, 'geographic_temporal'] = self.serialize_list_field(case_result.get('geographic_temporal', []))
                    progress_df.loc[case_mask, 'confidence_score'] = case_result.get('confidence_score', 0.0)
                    progress_df.loc[case_mask, 'classification_notes'] = case_result.get('notes', '')
            
            # Save progress
            progress_df.to_csv(progress_file, index=False)
            self.logger.info(f"Progress saved: {len(progress_df)} cases in {progress_file}")
            
        except Exception as e:
            self.logger.error(f"Failed to save progress: {str(e)}")

    def get_processed_cases_from_file(self, filename: str) -> Set[str]:
        """Get list of already processed case IDs from a CSV file"""
        try:
            if Path(filename).exists():
                df = pd.read_csv(filename)
                return set(df['Case'].values)
            return set()
        except Exception as e:
            self.logger.error(f"Error reading processed cases from {filename}: {str(e)}")
            return set()

    def load_schema(self, schema_file: str) -> Dict:
        """Load schema from JSON file"""
        with open(schema_file, 'r') as f:
            return json.load(f)

    def calculate_cost_estimate(self, iteration_sizes: List[int]) -> Dict:
        """Calculate cost estimate for all iterations"""
        input_cost_per_1k = 0.003
        output_cost_per_1k = 0.015
        
        total_cost = 0
        breakdown = {}
        
        for i, size in enumerate(iteration_sizes):
            # Schema discovery cost (only for first iteration)
            schema_cost = 0
            if i == 0:
                schema_tokens = 3000  # Estimate for schema discovery
                schema_cost = (schema_tokens / 1000) * (input_cost_per_1k + output_cost_per_1k)
            
            # Classification costs
            avg_input_tokens = 1000  # Prompt + case description + schema
            avg_output_tokens = 200   # JSON response
            
            iteration_input_cost = (size * avg_input_tokens / 1000) * input_cost_per_1k
            iteration_output_cost = (size * avg_output_tokens / 1000) * output_cost_per_1k
            iteration_total = schema_cost + iteration_input_cost + iteration_output_cost
            
            breakdown[f'iteration_{i+1}'] = {
                'cases': size,
                'schema_discovery_cost': schema_cost,
                'classification_cost': iteration_input_cost + iteration_output_cost,
                'total_cost': iteration_total
            }
            
            total_cost += iteration_total
        
        return {
            'breakdown': breakdown,
            'total_estimated_cost': total_cost
        }

# Main orchestration functions
async def run_iteration_1(classifier: SemiAutomatedCybercrimeClassifier, df: pd.DataFrame):
    """Run first iteration: 100 cases + schema discovery"""
    print("=== ITERATION 1: Schema Discovery + 100 cases ===")
    
    result_df, schema, processed_cases = await classifier.process_iteration(
        df, sample_size=100, excluded_cases=set(), 
        schema=None, iteration_name="1_discovery"
    )
    
    print(f"\nIteration 1 complete!")
    print(f"- Schema saved to: schema_1_discovery.json")
    print(f"- Results saved to: classified_1_discovery.csv") 
    print(f"- Processed {len(processed_cases)} cases")
    print(f"\nPrimary crime types found:")
    print(output_df['crime_type'].str.split(', ').explode().value_counts().head(10))
    print(f"\nAverage confidence: {result_df['confidence_score'].mean():.2f}")
    
    return processed_cases, schema

async def run_iteration_2(classifier: SemiAutomatedCybercrimeClassifier, df: pd.DataFrame, 
                         excluded_cases: Set[str], schema_file: str):
    """Run second iteration: 500 cases with modified schema"""
    print(f"\n=== ITERATION 2: 500 cases with refined schema ===")
    
    # Load human-modified schema
    schema = classifier.load_schema(schema_file)
    print(f"Loaded schema from: {schema_file}")
    
    result_df, _, new_processed_cases = await classifier.process_iteration(
        df, sample_size=500, excluded_cases=excluded_cases,
        schema=schema, iteration_name="2_validation"
    )
    
    print(f"\nIteration 2 complete!")
    print(f"- Results saved to: classified_2_validation.csv")
    print(f"- Processed {len(new_processed_cases)} cases")
    print(f"\nCrime types distribution:")
    print(result_df['crime_type'].str.split(', ').explode().value_counts().head(10))
    print(f"\nAverage confidence: {result_df['confidence_score'].mean():.2f}")
    
    return excluded_cases.union(new_processed_cases)

async def run_iteration_3(classifier: SemiAutomatedCybercrimeClassifier, df: pd.DataFrame,
                         excluded_cases: Set[str], schema_file: str):
    """Run final iteration: remaining ~17,400 cases"""
    remaining_count = len(df) - len(excluded_cases)
    print(f"\n=== ITERATION 3: Final {remaining_count} cases ===")
    
    # Load final schema
    schema = classifier.load_schema(schema_file)
    print(f"Loaded final schema from: {schema_file}")
    
    result_df, _, _ = await classifier.process_iteration(
        df, sample_size=remaining_count, excluded_cases=excluded_cases,
        schema=schema, iteration_name="3_final"
    )
    
    print(f"\nIteration 3 complete!")
    print(f"- Results saved to: classified_3_final.csv")
    print(f"- Processed {remaining_count} cases")
    print(f"\nFinal distribution:")
    print(result_df['crime_type'].str.split(', ').explode().value_counts().head(10))
    print(f"\nAverage confidence: {result_df['confidence_score'].mean():.2f}")

async def run_with_existing_schema():
    """Run classification using your existing schema"""
    # Initialize
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        print("❌ Error: ANTHROPIC_API_KEY environment variable not found!")
        print("Please set your Anthropic API key using one of these methods:")
        print("1. Export as environment variable: export ANTHROPIC_API_KEY='your-key-here'")
        print("2. Create a .env file with: ANTHROPIC_API_KEY=your-key-here")
        print("3. Set it in your shell: ANTHROPIC_API_KEY=your-key-here python semi_automated_classification.py")
        return
    
    # Validate API key format (basic check)
    if not api_key.startswith('sk-'):
        print("❌ Error: Invalid API key format. Anthropic API keys should start with 'sk-'")
        return
    
    classifier = SemiAutomatedCybercrimeClassifier(api_key)
    
    # Load data
    try:
        df = pd.read_csv("cyber_crime_cases.csv")
        print(f"✅ Loaded {len(df)} total cases")
    except FileNotFoundError:
        print("❌ Error: cyber_crime_cases.csv not found in current directory")
        return
    except Exception as e:
        print(f"❌ Error loading data: {str(e)}")
        return
    
    # Load your existing schema
    schema_file = "schema.json"  # Your schema file
    try:
        with open(schema_file, 'r') as f:
            schema = json.load(f)
        print(f"✅ Loaded schema from {schema_file}")
    except FileNotFoundError:
        print(f"❌ Error: {schema_file} not found in current directory")
        print("Please ensure schema.json exists or run schema discovery first")
        return
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in {schema_file}: {str(e)}")
        return
    except Exception as e:
        print(f"❌ Error loading schema: {str(e)}")
        return
    
    print("Schema categories and values:")
    if "schema" in schema:
        schema_content = schema["schema"]
    else:
        schema_content = schema
    
    for category, subcategories in schema_content.items():
        total_values = sum(len(values) for values in subcategories.values())
        print(f"  {category}: {len(subcategories)} subcategories, {total_values} total values")
        # Show a sample of values
        sample_values = []
        for subcat_values in list(subcategories.values())[:2]:  # First 2 subcategories
            sample_values.extend(subcat_values[:3])  # First 3 values from each
        print(f"    Sample values: {sample_values[:5]}")  # Show first 5 overall
    
    # Cost estimate for different batch sizes
    small_batch = 100
    medium_batch = 500 
    remaining = len(df) - small_batch - medium_batch
    
    cost_estimate = classifier.calculate_cost_estimate([small_batch, medium_batch, remaining])
    print(f"\nEstimated total cost: ${cost_estimate['total_estimated_cost']:.2f}")
    
    # Ask user which approach to take
    print(f"\nChoose approach:")
    print(f"1. Semi-automated (100 + 500 + {remaining} with human review)")
    print(f"2. Direct processing of sample (specify size)")
    print(f"3. Process all {len(df)} cases directly")
    
    choice = input("Enter choice (1/2/3): ").strip()
    
    if choice == "1":
        # Semi-automated approach
        await run_semi_automated_with_schema(classifier, df, schema)
    elif choice == "2":
        # Direct sample processing
        try:
            sample_size = int(input("Enter sample size: "))
            await run_direct_sample(classifier, df, schema, sample_size)
        except ValueError:
            print("❌ Invalid sample size. Please enter a number.")
    elif choice == "3":
        # Process all cases
        await run_full_processing(classifier, df, schema)
    else:
        print("❌ Invalid choice")

async def run_direct_sample(classifier, df, schema, sample_size):
    """Process a direct sample with your schema"""
    print(f"Processing {sample_size} random cases...")
    
    sample_df = df.sample(n=min(sample_size, len(df)), random_state=42)
    
    # Process using your schema
    result_df, _, _ = await classifier.process_iteration(
        df=pd.concat([sample_df]), 
        sample_size=len(sample_df),
        excluded_cases=set(),
        schema=schema,
        iteration_name="direct_sample"
    )
    
    print(f"Results saved to: classified_direct_sample.csv")
    
    # Show summary
    print("\nClassification Summary:")
    for category in ['crime_type', 'attack_vector', 'victim_approach']:
        if category in result_df.columns:
            print(f"\n{category.upper()}:")
            top_tags = result_df[category].str.split(', ').explode().value_counts().head(5)
            for tag, count in top_tags.items():
                print(f"  {tag}: {count}")

async def run_semi_automated_with_schema(classifier, df, schema):
    """Run semi-automated process but skip schema discovery since you have one"""
    print("=== SEMI-AUTOMATED PROCESSING WITH YOUR SCHEMA ===")
    
    # Stage 1: 100 cases with your schema
    print("\n=== STAGE 1: Testing with 100 cases ===")
    try:
        result_df_1, _, processed_1 = await classifier.process_iteration(
            df, sample_size=100, excluded_cases=set(),
            schema=schema, iteration_name="1_test"
        )
        print("Stage 1 complete! Please review 'classified_1_test.csv'")
    except Exception as e:
        print(f"Stage 1 interrupted: {str(e)}")
        print("Check progress_1_test.csv for partial results. You can resume this stage.")
        return
    
    input("Press Enter after review to continue...")
    
    # Stage 2: 500 cases
    print("\n=== STAGE 2: Validation with 500 cases ===")
    # Allow user to modify schema if needed
    schema_modified = input("Did you modify the schema? (y/N): ").strip().lower()
    if schema_modified == 'y':
        schema_file = input("Enter path to modified schema file: ").strip()
        with open(schema_file, 'r') as f:
            schema = json.load(f)
        print("Updated schema loaded")
    
    try:
        _, _, processed_2 = await classifier.process_iteration(
            df, sample_size=500, excluded_cases=processed_1,
            schema=schema, iteration_name="2_validation"
        )
        all_processed = processed_1.union(processed_2)
        print("Stage 2 complete! Please review 'classified_2_validation.csv'")
    except Exception as e:
        print(f"Stage 2 interrupted: {str(e)}")
        print("Check progress_2_validation.csv for partial results.")
        # Get what was actually processed for resume
        processed_2_partial = classifier.get_processed_cases_from_file("progress_2_validation.csv")
        all_processed = processed_1.union(processed_2_partial)
    
    input("Press Enter after review for final processing...")
    
    # Stage 3: Remaining cases
    remaining = len(df) - len(all_processed)
    print(f"\n=== STAGE 3: Final processing of {remaining} cases ===")
    
    try:
        await classifier.process_iteration(
            df, sample_size=len(df), excluded_cases=all_processed,
            schema=schema, iteration_name="3_final"
        )
        print("All processing complete!")
        print("Files: classified_1_test.csv, classified_2_validation.csv, classified_3_final.csv")
        
    except Exception as e:
        print(f"Stage 3 interrupted: {str(e)}")
        print("Progress saved. You can resume Stage 3 by running the script again.")
        print("The system will detect partial progress and continue from where it stopped.")

async def run_full_processing(classifier, df, schema):
    """Process all cases at once with your schema - with resume capability"""
    output_file = "classified_full_batch.csv"
    
    # Check if we should resume from existing progress
    if Path(output_file).exists():
        resume = input(f"Found existing {output_file}. Resume from where it left off? (Y/n): ").strip()
        if resume.lower() != 'n':
            print(f"Resuming processing...")
            await classifier.process_iteration(
                df, sample_size=len(df), excluded_cases=set(),
                schema=schema, iteration_name="full_batch", resume_from_file=output_file
            )
            print("Resumed processing complete!")
            return
    
    print(f"Processing all {len(df)} cases...")
    
    confirm = input(f"This will cost approximately $110-120. Continue? (y/N): ")
    if confirm.lower() != 'y':
        print("Cancelled")
        return
    
    try:
        await classifier.process_iteration(
            df, sample_size=len(df), excluded_cases=set(),
            schema=schema, iteration_name="full_batch"
        )
        print("Full processing complete! Results in: classified_full_batch.csv")
        
    except Exception as e:
        print(f"Processing interrupted: {str(e)}")
        print(f"Progress has been saved. You can resume by running the script again.")
        print(f"Check for progress_full_batch.csv file with partial results.")

if __name__ == "__main__":
    asyncio.run(run_with_existing_schema())