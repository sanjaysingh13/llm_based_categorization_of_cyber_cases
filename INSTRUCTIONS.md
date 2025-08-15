# Semi-Automated Cybercrime Classification Workflow

## Overview

This workflow uses a three-stage iterative approach to classify cybercrime cases using LLM (Claude) with human oversight and schema refinement. The goal is to achieve high-quality classifications while managing costs and allowing human experts to improve the system iteratively.

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

