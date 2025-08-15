# LLM-Based Cybercrime Case Classification

A semi-automated workflow for classifying cybercrime cases using LLM (Claude) with human oversight and iterative schema refinement.

## Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/sanjaysingh13/llm_based_categorization_of_cyber_cases.git
cd llm_based_categorization_of_cyber_cases
```

### 2. Set Up Virtual Environment
```bash
python3.12 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up API Key
Create a `.env` file in the project root:
```bash
echo "ANTHROPIC_API_KEY=your_api_key_here" > .env
```

## Workflow

### Before you begin, ensure you have a table of cases like mock_cyber_crime_cases.csv  ( Same column headings). Name it cyber_crime_cases.csv and put it in root folder (where mock_cyber_crime_cases.csv also exists).

### Stage 1: Initial Classification (100 cases)
```bash
python semi_automated_classification.py
```
- Processes first 100 cases to establish baseline schema
- Output: `classified_1_test.csv`

### Stage 2: Manual Review & Schema Update
1. **Examine Results**: Review `classified_1_test.csv` for quality and missing tags
2. **Update Schema**: Run the schema update script to automatically add new tags:
   ```bash
   python update_schema_from_results.py
   ```

### Stage 3: Validation (500 cases)
```bash
python semi_automated_classification.py
```
- Uses refined schema from Stage 2
- Output: `classified_2_validation.csv`

### Stage 4: Final Schema Refinement
1. **Review Validation Results**: Examine `classified_2_validation.csv`
2. **Final Schema Update**: Run schema update again if needed:
   ```bash
   python update_schema_from_results.py classified_2_validation.csv
   ```

### Stage 5: Full Processing
```bash
python semi_automated_classification.py
```
- Processes remaining ~17,400 cases with validated schema
- Output: `classified_3_final.csv`

### Stage 6: Analysis
```bash
python analyze_tag_distributions.py
```
- Generates comprehensive tag distribution analysis
- Output: `tag_analysis_results.json`

## Key Files

- `semi_automated_classification.py` - Main classification workflow
- `update_schema_from_results.py` - Automatic schema enhancement
- `analyze_tag_distributions.py` - Tag distribution analysis
- `schema.json` - Classification taxonomy (updated iteratively)
- `cyber_crime_cases.csv` - Input dataset

## Requirements

- Python 3.12+
- Anthropic API key (Claude)
- 8GB+ RAM for large datasets
- Stable internet connection

## Cost Estimate

- **Total Dataset**: ~$110-120
- **Stage 1**: ~$5-6 (100 cases)
- **Stage 2**: ~$25-30 (500 cases)  
- **Stage 3**: ~$80-85 (remaining cases)

## Documentation

- **`INSTRUCTIONS.md`** - Detailed workflow documentation and technical details
- **`RELEASE_NOTES.md`** - Version information, features, and system requirements

## Support

For detailed workflow information, see `INSTRUCTIONS.md`.
