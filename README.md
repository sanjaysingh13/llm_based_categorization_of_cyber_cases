# LLM-Based Cybercrime Case Classification

A semi-automated workflow for classifying cybercrime cases using LLM (Claude) with human oversight and iterative schema refinement.

## Why?
The universe of cybercrimes can be bewildering, even to seasoned police officers. Cyber Crime Wing, West Bengal felt the need to, first of all classify the 18,000 odd cybercrimes in our database according to the features of the crime, like type of incident, the attack vector, the path of approaching the victim, technology used, victim demographics and the principles behind the social engineering. 18,000 is a big number to take on manually, so we planned to use LLMs to do it for us. Our input is basically the gist of the FIR. Because there are costs involved (about $150 for 20,000 cases), we made it a 3-step process to see how reliable the LLM's classification is. The first 2 steps processed samples of 100 and 500 cases respectively. A "human-in-the-loop" then reviewed those classifications for every case in the sample with two main tasks:
1. Add or change tags to a case.
2. Modify the custom instruction to the LLM from a human's (LEA) perspective.

We found the output reasonably good. But LLM sometimes misses the policing context. For instance, it was unable for it to comprehend what "Digital Arrest" was. It kept classifying it as "impersonation_of_authority".
That's why we need to give it custom instructions like :

"8. If a person has been put under fear by a perpetrator, pretending to be a government official, by mentioning that his identity has been used for a crime, or that a parcel in his name has contraband, or something similar, add 'digital_arrest' to the classification, even if the words are not specifically mentioned."

or:

"16. 'AEPS_fraud' is a similar local type of cybercrime involving Aadhar Enabled Payment System. Money can be withdrawn from the victim's account by using the victim's Aadhar number and biometrics, by obtaining the biometric data of the victim illegally."

Our initial sample analysis results are like this table:
https://github.com/sanjaysingh13/llm_based_categorization_of_cyber_cases/blob/main/INSTRUCTIONS.md#tag-distribution-table

You can use this open source code being provided by CCW, West Bengal. Prerequisites  are Python and a Claude API.

## Benefits
Once we have done  this:
1) We can segment and analyse past cases.
2) Automatically tag all newly reported cases.
3) Monitor seasonal variation of a particular class of cybercrime and synchronise our tailored public awareness campaigns to match with that.

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

Before you begin, replace `mock_cyber_crime_cases.csv` with your cybercrime data, and rename it `cyber_crime_cases.csv`

### Stage 1: Initial Classification (100 cases)
```bash
python semi_automated_classification.py
```
- Processes first 100 cases (randomly sampled) to establish baseline schema
- Output: `classified_1_test.csv`

### Stage 2: Manual Review & Schema Update
1. **Examine Results**: Review `classified_1_test.csv` for quality and missing tags.
If you want to change any instructions to Claude, modify  [`specific_instructions.py`](https://github.com/sanjaysingh13/llm_based_categorization_of_cyber_cases/blob/main/specific_instructions.py)
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
- Processes remaining  cases  (~17,400 in our database) with validated schema
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

- **[`INSTRUCTIONS.md`](https://github.com/sanjaysingh13/llm_based_categorization_of_cyber_cases/blob/main/INSTRUCTIONS.md)** - Detailed workflow documentation and technical details
- **[`RELEASE_NOTES.md`](https://github.com/sanjaysingh13/llm_based_categorization_of_cyber_cases/blob/main/RELEASE_NOTES.md)** - Version information, features, and system requirements

## Support

For detailed workflow information, see [`INSTRUCTIONS.md`](https://github.com/sanjaysingh13/llm_based_categorization_of_cyber_cases/blob/main/INSTRUCTIONS.md).
