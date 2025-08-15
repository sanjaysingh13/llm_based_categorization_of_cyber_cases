# Semi-Automated Cybercrime Classification Workflow

## Overview

This workflow uses a three-stage iterative approach to classify cybercrime cases using LLM (Claude) with human oversight and schema refinement. The goal is to achieve high-quality classifications while managing costs and allowing human experts to improve the system iteratively.

## Tag Distribution Analysis and Expected Output Patterns

### Current Dataset Analysis Summary
Based on analysis of 609 classified cybercrime cases (101 from test + 508 from validation), here are the expected tag distributions across classification categories:


### Expected Output Quality Indicators

#### High Confidence Cases (0.9-1.0)
- Clear attack patterns with well-documented methods
- Specific technology platforms and communication channels
- Detailed financial impact and transaction records
- Clear victim demographics and approach methods

#### Medium Confidence Cases (0.7-0.8)
- Some missing details in attack methodology
- Limited information about victim approach
- Unclear technology platforms used
- Partial social engineering technique identification

#### Low Confidence Cases (0.4-0.6)
- Limited case details in original complaint
- Unclear attack vectors or methods
- Missing victim demographic information
- Ambiguous classification requirements

### Classification Consistency Guidelines

#### Crime Type Classification
- **Primary Type**: Always assign the most dominant crime type
- **Secondary Types**: Add additional types if multiple patterns exist
- **Financial Impact**: Prioritize financial fraud types for monetary losses
- **Privacy Violations**: Classify non-consensual imagery and data breaches appropriately

#### Attack Vector Identification
- **Primary Method**: Identify the main attack technique used
- **Technical vs Social**: Distinguish between technical attacks and social engineering
- **Impersonation Types**: Specify whether it's authority, corporate, or personal impersonation
- **Access Methods**: Clarify how unauthorized access was gained

#### Victim Approach Classification
- **Communication Channel**: Identify the primary platform used for initial contact
- **Approach Method**: Distinguish between cold calls, social media, and other methods
- **Trust Building**: Note if relationship building was involved
- **Urgency Creation**: Identify pressure tactics used

#### Technology Platform Mapping
- **Primary Platform**: Identify the main technology used
- **Communication Tools**: Note messaging and social media platforms
- **Financial Platforms**: Specify banking and payment systems
- **Trading Platforms**: Identify investment and trading applications

#### Victim Demographics Assessment
- **Tech Familiarity**: Classify based on behavior patterns and responses
- **Age Groups**: Use available age information when provided
- **Professional Status**: Note occupation and business context
- **Vulnerability Factors**: Consider factors that made victims susceptible

#### Impact Outcome Classification
- **Primary Impact**: Identify the main consequence suffered
- **Financial Losses**: Quantify monetary and investment losses
- **Privacy Breaches**: Note data and reputation damage
- **Emotional Impact**: Consider psychological and social consequences

#### Social Engineering Technique Identification
- **Primary Technique**: Identify the main manipulation method
- **Pressure Tactics**: Note authority, threat, or time pressure used
- **Trust Building**: Identify relationship and credibility establishment
- **Credential Manipulation**: Note fake credentials and impersonation details

#### Geographic-Temporal Pattern Classification
- **Operation Duration**: Classify as quick hit or sustained operation
- **Geographic Scope**: Note local, interstate, or cross-border operations
- **Cyber Space Usage**: Identify online vs. offline components
- **Temporal Patterns**: Note timing and duration of operations

### Quality Assurance Recommendations

#### For Human Reviewers
1. **Check Tag Consistency**: Ensure similar cases receive similar classifications
2. **Validate Confidence Scores**: High confidence should correlate with detailed case information
3. **Review Edge Cases**: Pay attention to unusual crime types or attack methods
4. **Verify Platform Accuracy**: Ensure technology platforms match case descriptions

#### For Schema Updates
1. **Add Missing Tags**: Include new crime types and attack vectors as they emerge
2. **Refine Categories**: Split overly broad categories into more specific subcategories
3. **Update Examples**: Provide clear examples for each classification category
4. **Maintain Balance**: Ensure categories have sufficient granularity without being too specific

#### For Classification Process
1. **Use Consistent Naming**: Maintain standardized tag names across all categories
2. **Apply Multiple Tags**: Use multiple tags when cases involve multiple patterns
3. **Prioritize Primary Types**: Always identify the main crime type and attack method
4. **Document Reasoning**: Provide clear notes explaining classification decisions

This analysis provides a baseline understanding of expected tag distributions and helps ensure consistent classification quality across the dataset.

### Complete Tag Distribution Analysis Results

The following table provides the complete breakdown of all tags and their distributions across the 609 analyzed cases. **Percentages represent the proportion of cases where each tag appears (out of 609 total cases):**

| Category | Tag | Count | Percentage | Category | Tag | Count | Percentage |
|----------|-----|-------|------------|----------|-----|-------|------------|
| **Crime Type** | | | | **Attack Vector** | | | |
| | financial_fraud | 229 | 37.6% | | impersonation | 287 | 47.13% |
| | account_takeover | 157 | 25.78% | | unauthorized_access | 155 | 25.45% |
| | customer_service_fraud | 148 | 24.3% | | false_business_proposal | 144 | 23.65% |
| | credential_theft | 113 | 18.56% | | credential_theft | 130 | 21.35% |
| | traditional_cheating_and_fraud | 100 | 16.42% | | authority_abuse | 99 | 16.26% |
| | privacy_violation | 73 | 11.99% | | corporate_impersonation | 73 | 11.99% |
| | investment_scam | 68 | 11.17% | | relationship_building | 63 | 10.34% |
| | non_consensual_imagery | 63 | 10.34% | | otp_fraud | 51 | 8.37% |
| | sexual_blackmail | 44 | 7.22% | | malicious_app | 50 | 8.21% |
| | job_fraud | 41 | 6.73% | | account_takeover | 47 | 7.72% |
| | loan_fraud | 37 | 6.08% | | phishing_link | 40 | 6.57% |
| | bank_kyc_fraud | 37 | 6.08% | | remote_access_app | 40 | 6.57% |
| | unauthorized_access | 33 | 5.42% | | kyc_pretext | 34 | 5.58% |
| | provocative_social_media_post | 28 | 4.6% | | fake_google_search_results | 15 | 2.46% |
| | task_based_fraud | 27 | 4.43% | | fake_mobile_tower_installation | 15 | 2.46% |
| | document_forgery | 27 | 4.43% | | qr_code_for_debiting_fraudulently_presented_as_crediting | 7 | 1.15% |
| | reputation_threat | 27 | 4.43% | | sim_swap | 5 | 0.82% |
| | fraud_by_impersonation_of_influential_person | 24 | 3.94% | | atm_manipulation | 4 | 0.66% |
| | stock_market_scam | 17 | 2.79% | | facebook_ad | 3 | 0.49% |
| | sextortion | 13 | 2.13% | | credit_card_courier_involvement | 1 | 0.16% |
| | identity_crimes | 12 | 1.97% | | fake_website | 1 | 0.16% |
| | franchise_fraud | 11 | 1.81% | | threat_pressure | 1 | 0.16% |
| | call_centre_fraud | 10 | 1.64% | | | | | |
| | digital_arrest | 10 | 1.64% | **Victim Approach** | | | |
| | extortion | 9 | 1.48% | | cold_call | 254 | 41.71% |
| | fake_hotel_booking | 8 | 1.31% | | whatsapp_message | 99 | 16.26% |
| | recording_of_sexual_video_call_inititiated_by_perpetrator | 8 | 1.31% | | social_media_friend_request | 70 | 11.49% |
| | sim_card_fraud | 8 | 1.31% | | direct_contact | 51 | 8.37% |
| | not_a_cyber_crime | 6 | 0.99% | | sms_contact | 31 | 5.09% |
| | subsidy_fraud | 5 | 0.82% | | marketplace_listing | 27 | 4.43% |
| | fake_sim_card_pos | 5 | 0.82% | | telegram_invite | 22 | 3.61% |
| | ransom_demand | 4 | 0.66% | | fake_google_search_results | 15 | 2.46% |
| | child_exploitation | 4 | 0.66% | | job_portal | 13 | 2.13% |
| | online_gambling | 2 | 0.33% | | facebook_ad | 3 | 0.49% |
| | romance_fraud | 2 | 0.33% | | mail | 1 | 0.16% |
| | fake_wine_delivery_fraud | 1 | 0.16% | | nigerian scam | 1 | 0.16% |
| | fake_service_fraud | 1 | 0.16% | | youtube_ad | 1 | 0.16% |
| | call_forwarding_to_divert_otp_over_call | 1 | 0.16% | | dating_app_match | 1 | 0.16% |
| | general_purpose_fir_suitable_for_wider_investigation | 1 | 0.16% | | | | | |
| | victim_was_paid_from_proceeds_of_crime | 1 | 0.16% | **Technology Platform** | | | |
| | failure_to_deliver_purchased_goods | 1 | 0.16% | | banking_apps | 306 | 50.25% |
| | child_sexual_abuse_material | 1 | 0.16% | | whatsapp | 113 | 18.56% |
| | fake_advertisement_for_product_sales | 1 | 0.16% | | facebook | 90 | 14.78% |
| | doctored_media | 1 | 0.16% | | upi_apps | 79 | 12.97% |
| | csp_fraud | 1 | 0.16% | | credit_card | 60 | 9.85% |
| | suo_moto_case | 1 | 0.16% | | sms | 48 | 7.88% |
| | | | | | | trading_apps | 27 | 4.43% |
| **Victim Demographics** | | | | | telegram | 22 | 3.61% |
| | novice | 366 | 60.1% | | instagram | 16 | 2.63% |
| | middle_aged | 99 | 16.26% | | youtube | 9 | 1.48% |
| | professional | 87 | 14.29% | | crypto_platforms | 4 | 0.66% |
| | young_adult | 81 | 13.3% | | social_media | 4 | 0.66% |
| | business_owner | 42 | 6.9% | | telephone | 1 | 0.16% |
| | intermediate | 27 | 4.43% | | twitter | 1 | 0.16% |
| | elderly | 19 | 3.12% | | | | | |
| | student | 14 | 2.3% | **Impact Outcome** | | | |
| | minor | 10 | 1.64% | | direct_monetary_loss | 489 | 80.3% |
| | retired | 9 | 1.48% | | unauthorized_transactions | 275 | 45.16% |
| | advanced | 1 | 0.16% | | reputation_damage | 105 | 17.24% |
| | adult | 1 | 0.16% | | privacy_breach | 87 | 14.29% |
| | | | | | | emotional_trauma | 86 | 14.12% |
| **Social Engineering** | | | | | investment_loss | 71 | 11.66% |
| | impersonation | 278 | 45.65% | | identity_compromise | 43 | 7.06% |
| | fake_credentials | 241 | 39.57% | | credit_damage | 10 | 1.64% |
| | authority_pressure | 202 | 33.17% | | harassment | 1 | 0.16% |
| | opportunity_fomo | 102 | 16.75% | | | | | |
| | gradual_investment | 98 | 16.09% | **Geographic-Temporal** | | | |
| | threat_pressure | 87 | 14.29% | | quick_hit | 321 | 52.71% |
| | relationship_building | 46 | 7.55% | | cyber_space | 295 | 48.44% |
| | false_testimonials | 34 | 5.58% | | local | 291 | 47.78% |
| | time_pressure | 7 | 1.15% | | multiple_day_operation | 120 | 19.7% |
| | trust_building | 4 | 0.66% | | sustained_fraud | 115 | 18.88% |
| | authority_abuse | 1 | 0.16% | | interstate | 28 | 4.6% |
| | | | | | | cross_border | 23 | 3.78% |

**Summary Statistics:**
- **Total Cases Analyzed**: 609 (101 test + 508 validation)
- **Crime Type Tags**: 229 unique tags across 608 cases
- **Attack Vector Tags**: 287 unique tags across 598 cases  
- **Victim Approach Tags**: 254 unique tags across 505 cases
- **Technology Platform Tags**: 306 unique tags across 545 cases
- **Victim Demographics Tags**: 366 unique tags across 560 cases
- **Impact Outcome Tags**: 489 unique tags across 604 cases
- **Social Engineering Tags**: 278 unique tags across 506 cases
- **Geographic-Temporal Tags**: 321 unique tags across 608 cases

### Tag Distribution Analysis Script Usage

The `analyze_tag_distributions.py` script provides ongoing analysis capabilities for monitoring classification quality and consistency:

#### Script Features
- **Multi-Dataset Analysis**: Analyzes individual datasets or combined results
- **Percentage Calculations**: Shows tag frequency distributions across all categories
- **JSON Export**: Saves analysis results for further processing
- **Robust CSV Parsing**: Handles various CSV formats and parsing issues
- **Comprehensive Reporting**: Provides detailed breakdowns for each classification category

#### Usage Instructions
```bash
# Basic usage - analyzes all available datasets
python analyze_tag_distributions.py

# The script will automatically:
# 1. Load classified_1_test.csv (if available)
# 2. Load classified_2_validation.csv (if available)
# 3. Generate combined analysis
# 4. Save results to tag_analysis_results.json
```

#### Output Files
- **Console Output**: Detailed tag distribution tables for each category
- **tag_analysis_results.json**: Structured JSON with complete analysis data
- **Progress Information**: Loading status and dataset statistics

#### When to Use the Script
1. **After Each Stage**: Analyze results to identify classification patterns
2. **Quality Monitoring**: Check for consistency in tag usage
3. **Schema Validation**: Ensure new tags are being used appropriately
4. **Progress Tracking**: Monitor classification quality improvements
5. **Report Generation**: Create summaries for stakeholders

#### Interpreting Results
- **High Percentage Tags**: Indicate common patterns that should be well-represented in schema
- **Low Percentage Tags**: May represent edge cases or emerging threat patterns
- **Tag Distribution Balance**: Helps identify if categories need more granularity
- **Consistency Patterns**: Reveals if similar cases receive similar classifications

#### Customization Options
The script can be modified to:
- Analyze specific datasets by changing file paths
- Focus on particular classification categories
- Export results in different formats
- Generate visualizations of tag distributions
- Compare results across different time periods

This analysis tool helps maintain classification quality and provides insights for continuous improvement of the classification system.

## Workflow Stages

### Stage 1: Schema Discovery + Initial Testing (100 cases)
**Purpose:** Establish baseline classification schema and test the system
**Process:**
1. **Schema Discovery:** LLM analyzes first 100 cases to create initial classification taxonomy
2. **Initial Classification:** All 100 cases are classified using the discovered schema
3. **Human Review:** Expert reviews results and identifies areas for improvement
4. **Schema Enhancement:** Expert can modify the schema file to add missing categories/values

**Output Files:**
- `classified_1_test.csv` - Results of first 100 cases
- `progress_1_test.csv` - Progress tracking (deleted after completion)

**Key Benefits:**
- Establishes baseline classification quality
- Identifies gaps in the initial schema
- Allows human experts to improve the taxonomy before larger batches

### Stage 2: Validation with Refined Schema (500 cases)
**Purpose:** Validate improved schema on larger dataset
**Process:**
1. **Schema Loading:** Uses the enhanced schema from Stage 1
2. **Batch Processing:** Classifies 500 new cases (excluding Stage 1 cases)
3. **Quality Assessment:** Evaluates classification consistency and accuracy
4. **Final Schema Refinement:** Expert can make final adjustments if needed

**Output Files:**
- `classified_2_validation.csv` - Results of 500 validation cases
- `progress_2_validation.csv` - Progress tracking (deleted after completion)

**Key Benefits:**
- Tests schema improvements on larger dataset
- Identifies any remaining classification issues
- Provides confidence in schema quality before full processing

### Stage 3: Full Processing (Remaining ~17,400 cases)
**Purpose:** Process all remaining cases with validated schema
**Process:**
1. **Final Schema:** Uses the refined schema from previous stages
2. **Bulk Processing:** Handles remaining cases with established taxonomy
3. **Completion:** Produces final classified dataset

**Output Files:**
- `classified_3_final.csv` - Final results for all remaining cases

## How the System Works

### Schema Structure
The classification schema is hierarchical with main categories and subcategories:

```json
{
  "crime_type": {
    "financial_fraud": ["investment_scam", "job_fraud", "loan_fraud"],
    "identity_crimes": ["sim_card_fraud", "account_takeover"]
  },
  "attack_vector": {
    "technical": ["phishing_link", "malicious_app"],
    "social": ["impersonation", "relationship_building"]
  }
  // ... other categories
}
```

### Classification Process
1. **Prompt Engineering:** Each case gets a detailed prompt including:
   - Case description and ID
   - Full hierarchical schema
   - Flattened value lists for easy selection
   - Clear classification rules and examples

2. **LLM Processing:** Claude analyzes each case and returns:
   - Specific values from schema (not subcategory names)
   - Confidence score (0.0-1.0)
   - Additional notes and reasoning

3. **Error Handling:** Robust error handling for:
   - API failures
   - Rate limiting
   - JSON parsing errors
   - Network issues

### Resume Capability
The system includes comprehensive resume functionality:
- **Progress Tracking:** Saves intermediate results after each batch
- **Checkpoint Files:** Tracks processing state and metadata
- **Automatic Detection:** Identifies already processed cases
- **Seamless Continuation:** Resumes from exact stopping point

## Human Expert Role

### During Stage 1 Review
**What to Review:**
- Classification accuracy and completeness
- Missing or incorrect tags
- Schema coverage gaps
- Confidence score patterns

**What to Improve:**
- Add missing crime types, attack vectors, etc.
- Refine category definitions
- Add new subcategories for emerging patterns
- Correct obvious misclassifications

**How to Improve:**
- **Manual CSV Editing:** You can directly edit tags in `classified_1_test.csv` rows
- **Schema Updates:** Use the `update_schema_from_results.py` script to automatically add new tags to `schema.json`
- **Direct Schema Editing:** Manually edit `schema.json` if you prefer JSON editing

### Schema Enhancement Process
1. **Edit `schema.json`** to add missing elements (this is your existing schema file)
2. **Add new categories/values** that would improve classification
3. **Refine existing categories** for better precision
4. **Ensure consistency** in naming and structure

**Important Note:** The workflow uses your existing `schema.json` file throughout all stages. There is no `schema_1_discovery.json` file generated - the system loads and uses your pre-existing schema as the foundation.

### Value Addition
Manual improvements provide:
- **Domain Expertise:** Human understanding of cybercrime patterns
- **Schema Completeness:** Coverage of edge cases and emerging threats
- **Classification Quality:** Better training data for subsequent stages
- **Cost Efficiency:** Fewer API calls needed for corrections

## Technical Features

### Batch Processing
- **Small Batches:** 5 cases per batch for frequent saves
- **Progress Persistence:** Automatic saving after each batch
- **Error Isolation:** Individual case failures don't stop processing
- **Rate Limiting:** Built-in delays to avoid API limits

### Schema Management
- **Automatic Updates:** `update_schema_from_results.py` script automatically adds new tags from CSV results
- **Flexible Input:** Script can analyze any stage's results (`classified_1_test.csv`, `classified_2_validation.csv`, etc.)
- **Backup Protection:** Creates `schema_backup.json` before making changes
- **Smart Integration:** New tags are added to appropriate categories based on CSV column headers

### Data Management
- **Safe Serialization:** Handles list fields and special characters
- **Error Recovery:** Graceful handling of malformed data
- **Backup Files:** Progress files for resume capability
- **Clean Output:** Final results in clean, structured format

### Cost Management
- **Token Optimization:** Efficient prompts and responses
- **Batch Sizing:** Optimal balance of speed vs. cost
- **Resume Capability:** Avoids reprocessing completed work
- **Cost Estimation:** Pre-processing cost calculations

## Best Practices

### For Human Reviewers
1. **Focus on Schema Quality:** This has the biggest impact on subsequent stages
2. **Look for Patterns:** Identify recurring classification issues
3. **Validate Edge Cases:** Ensure schema covers unusual but important scenarios
4. **Maintain Consistency:** Use consistent naming conventions

### For System Operation
1. **Monitor Progress Files:** Check for any processing issues
2. **Validate Schema Changes:** Ensure JSON format remains valid
3. **Backup Important Files:** Keep copies of improved schemas
4. **Test Small Batches:** Verify improvements before large-scale processing

## Expected Outcomes

### Quality Improvements
- **Stage 1:** Baseline quality with identified gaps
- **Stage 2:** Improved consistency with refined schema
- **Stage 3:** High-quality classifications across full dataset

### Iterative Schema Enhancement
- **Stage 1 → Stage 2:** Schema improved based on 100-case review
- **Stage 2 → Stage 3:** Schema further refined based on 500-case validation
- **Continuous Learning:** Each stage builds upon previous improvements
- **Human Expertise Integration:** Manual insights automatically incorporated into schema

### Cost Efficiency
- **Total Estimated Cost:** $110-120 for full dataset
- **Iterative Refinement:** Reduces need for post-processing corrections
- **Human Expertise:** Leverages domain knowledge without manual classification

### Final Deliverable
- **Complete Dataset:** All cases classified with consistent taxonomy
- **Validated Schema:** Human-reviewed and tested classification system
- **Quality Metrics:** Confidence scores and classification notes for analysis
- **Process Documentation:** Reusable workflow for future datasets

## Troubleshooting

### Common Issues
- **API Key Problems:** Check format and environment variables
- **Rate Limiting:** System automatically handles with delays
- **Schema Errors:** Validate JSON format before proceeding
- **Processing Interruptions:** Use resume functionality to continue

### Schema Update Issues
- **File Paths:** `update_schema_from_results.py` expects files in current directory
- **CSV Format:** Ensure classification columns match expected names
- **Schema Validation:** Script creates backup before making changes
- **New Tag Integration:** Tags are automatically categorized based on CSV column structure

### Recovery Steps
1. **Check Progress Files:** Look for partial results
2. **Validate Schema:** Ensure JSON is properly formatted
3. **Resume Processing:** System will detect and continue from stopping point
4. **Monitor Logs:** Check for specific error messages

### Schema Update Workflow
1. **Review Results:** Examine classification output CSV for quality and missing tags
2. **Manual Edits:** Add/improve tags directly in CSV rows if needed
3. **Run Update Script:** Execute `python update_schema_from_results.py [filename.csv]`
4. **Verify Changes:** Check `schema.json` for new tags and `schema_backup.json` for safety
5. **Continue Processing:** Resume main workflow with improved schema

This workflow balances automation with human expertise, allowing for iterative improvement while maintaining cost efficiency and data quality.

